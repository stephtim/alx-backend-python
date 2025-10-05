# chats/signals.py
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    When a Message is created, create a Notification for the receiver.
    Use transaction.on_commit to avoid race conditions when signals fire inside transactions.
    """
    if not created or instance.sender_id == instance.receiver_id:
        return
    def _create_notification():
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            actor=instance.sender,
            verb='sent you a message'
        )
    transaction.on_commit(_create_notification)

@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    """
    Before a Message is saved, if the content changed, record the old content in MessageHistory.
    We schedule creation with transaction.on_commit so history is not created if the outer
    transaction rolls back.
    """
    if not instance.pk:
        return
    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    if old.content == instance.content:
        return
    old_content = old.content
    editor = getattr(instance, '_editor', None) or getattr(instance, 'edited_by', None)
    def _create_history():
        prev_count = MessageHistory.objects.filter(message_id=instance.pk).count()
        MessageHistory.objects.create(
            message_id=instance.pk,
            old_content=old_content,
            edited_by=editor if getattr(editor, 'pk', None) else None,
            version=prev_count + 1
        )
    transaction.on_commit(_create_history)
    instance.edited = True
    instance.edited_at = timezone.now()
    instance.edit_count = (old.edit_count or 0) + 1

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    After a User is deleted, remove any leftover related objects not already handled by CASCADE (e.g., edited_by links).
    """
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()