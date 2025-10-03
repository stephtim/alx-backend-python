# chats/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    When a Message is created, create a Notification for the receiver.
    Use transaction.on_commit to avoid race conditions when signals fire inside transactions.
    """
    if not created:
        return

    def _create_notification():
        # don't notify if sender == receiver
        if instance.sender_id == instance.receiver_id:
            return
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            actor=instance.sender,
            verb='sent you a message'
        )

    transaction.on_commit(_create_notification)
