# chats/tests.py
#!/usr/bin/env python3
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()


class MessageNotificationTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username="alice", password="password123"
        )
        self.receiver = User.objects.create_user(
            username="bob", password="password123"
        )

    def test_notification_created_on_message(self):
        """A Notification should be created when a new Message is sent."""
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hi Bob!"
        )

        notification = Notification.objects.filter(user=self.receiver).first()

        self.assertIsNotNone(notification)
        self.assertEqual(notification.message, msg)
        self.assertEqual(notification.actor, self.sender)
        self.assertEqual(notification.user, self.receiver)
        self.assertFalse(notification.is_read)

    def test_no_notification_if_sender_is_receiver(self):
        """No notification should be created if sender == receiver."""
        Message.objects.create(
            sender=self.sender,
            receiver=self.sender,
            content="Talking to myself"
        )

        notif_count = Notification.objects.filter(user=self.sender).count()
        self.assertEqual(notif_count, 0)
