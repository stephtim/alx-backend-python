from django.test import TestCase

# Create your tests here.
#!/usr/bin/env python3
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Message, Notification, MessageHistory

User = get_user_model()

class UserDeletionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='to_delete', password='pass123')
        self.receiver = User.objects.create_user(username='receiver', password='pass123')
        self.client.login(username='to_delete', password='pass123')

        msg = Message.objects.create(sender=self.user, receiver=self.receiver, content="Hello")
        Notification.objects.create(user=self.receiver, actor=self.user, message=msg, verb="sent you a message")
        MessageHistory.objects.create(message=msg, old_content="Hello", edited_by=self.user, version=1)

    def test_user_deletion_cleans_related_data(self):
        response = self.client.delete('/api/delete-account/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username='to_delete').exists())
        self.assertEqual(Message.objects.filter(sender__username='to_delete').count(), 0)
        self.assertEqual(Notification.objects.filter(actor__username='to_delete').count(), 0)
        self.assertEqual(MessageHistory.objects.filter(edited_by__username='to_delete').count(), 0)
