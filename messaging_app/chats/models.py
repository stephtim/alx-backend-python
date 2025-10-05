from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
import uuid
from messaging_app.messaging_app import settings


class UserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, first_name="", last_name="", **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name="", last_name="", **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, first_name, last_name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that meets the provided database specification.

    Fields:
      - user_id (UUID primary key)
      - first_name, last_name (NOT NULL)
      - email (unique, indexed)
      - password (inherited from AbstractBaseUser) - stores hashed password
      - password_hash (duplicate of hashed password for schema compatibility)
      - phone_number (nullable)
      - role (enum)
      - created_at (timestamp)
    """

    ROLE_GUEST = "guest"
    ROLE_HOST = "host"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = [
        (ROLE_GUEST, "Guest"),
        (ROLE_HOST, "Host"),
        (ROLE_ADMIN, "Admin"),
    ]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=150)   # NOT NULL by default (blank=False)
    last_name = models.CharField(max_length=150)
    # We keep Django's `password` field (inherited) which holds the hashed password.
    # We also maintain a separate column `password_hash` to match the schema exactly.
    password_hash = models.CharField(max_length=128, editable=False)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_GUEST)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        constraints = [
            models.UniqueConstraint(fields=["email"], name="uq_users_email"),
        ]
        indexes = [
            models.Index(fields=["email"], name="ix_users_email"),
        ]

    def __str__(self):
        return f"{self.email}"

    def set_password(self, raw_password):
        """
        Override set_password so that we keep password_hash column in sync
        with Django's built-in password field (which stores the hashed password).
        Note: this does NOT save the model; caller should call save() when needed.
        """
        super().set_password(raw_password)
        # `self.password` now contains the hashed password string (algorithm$salt$hash)
        self.password_hash = self.password


class Conversation(models.Model):
    """
    Conversation with UUID PK and participants relation.
    """

    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "conversations"
        verbose_name = "conversation"
        verbose_name_plural = "conversations"
        indexes = [
            models.Index(fields=["created_at"], name="ix_conversations_created_at"),
        ]

    def __str__(self):
        # Short representation
        return f"Conversation {self.conversation_id}"


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False)

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edit_count = models.PositiveIntegerField(default=0)
    read = models.BooleanField(default=False, db_index=True)

    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager

    def __str__(self):
        parent = f" reply to {self.parent_message_id}" if self.parent_message_id else ""
        return f"Message {self.pk}{parent} [{self.sender} → {self.receiver}]"

    @staticmethod
    def fetch_threaded_messages(root_message_id):
        """
        Recursively fetch all replies to a message and return them in a threaded format.
        """
        def get_replies(message):
            replies = list(message.replies.select_related('sender', 'receiver').prefetch_related('replies'))
            return [
                {
                    'message': reply,
                    'replies': get_replies(reply)
                }
                for reply in replies
            ]
        try:
            root = Message.objects.select_related('sender', 'receiver').prefetch_related('replies').get(pk=root_message_id)
        except Message.DoesNotExist:
            return None
        return {
            'message': root,
            'replies': get_replies(root)
        }

    class Meta:
        db_table = "messages"
        verbose_name = "message"
        verbose_name_plural = "messages"
        indexes = [
            models.Index(fields=["timestamp"], name="ix_messages_timestamp"),
            models.Index(fields=["receiver"], name="ix_messages_receiver"),
            models.Index(fields=["read"], name="ix_messages_read"),
        ]


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='actor_notifications'
    )
    verb = models.CharField(max_length=255, default='sent you a message')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif {self.pk} → {self.user}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='histories'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='message_edits'
    )
    version = models.PositiveIntegerField()

    class Meta:
        ordering = ['-version']
        unique_together = ('message', 'version')

    def __str__(self):
        return f"History v{self.version} of Message {self.message_id}"