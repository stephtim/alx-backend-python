from django.db import models

# Create your models here.
# chats/models.py
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
import uuid


class User(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    # Use a CharField with choices for the role
    ROLE_CHOICES = (
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")
    email = models.EmailField(unique=True)

    # Override the built-in fields to match the schema
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    # Set a password hash field that will be managed by Django's auth system
    password_hash = models.CharField(max_length=128)

    # Set up created_at field
    created_at = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

class UserManager(BaseUserManager):
    """
    Manager for the custom User model. Creates users and superusers.
    """

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
        # set_password will populate password_hash as well (see User.set_password)
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


class Message(models.Model):
    """
    Message model as specified.
    """

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(User, related_name="messages_sent", on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "messages"
        verbose_name = "message"
        verbose_name_plural = "messages"
        indexes = [
            models.Index(fields=["sent_at"], name="ix_messages_sent_at"),
            # Useful index if you query messages by conversation often
            models.Index(fields=["conversation"], name="ix_messages_conversation"),
        ]

    def __str__(self):
        return f"Message {self.message_id} by {self.sender.email}"