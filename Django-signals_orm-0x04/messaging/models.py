# chats/models.py
from django.conf import settings
from django.db import models

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

    def __str__(self):
        return f"Message {self.pk} from {self.sender} → {self.receiver}"
    
    # Edit tracking
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edit_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Message {self.pk} from {self.sender} → {self.receiver}"

class MessageHistory(models.Model):
    """
    Stores previous versions of a Message. 'version' increments (1 = first saved history).
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='histories')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='message_edits'
    )
    version = models.PositiveIntegerField()

    class Meta:
        ordering = ['-version']
        unique_together = ('message', 'version')

    def __str__(self):
        return f"History v{self.version} of Message {self.message_id}"


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

    class Meta:
        ordering = ['-created_at']

    def mark_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"Notification for {self.user}: {self.verb}"
