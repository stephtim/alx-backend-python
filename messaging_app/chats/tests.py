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

#!/usr/bin/env python3
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Message, MessageHistory, Notification

User = get_user_model()

class ThreadingAndCleanupTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # users
        self.alice = User.objects.create_user(username='alice', password='pass')
        self.bob = User.objects.create_user(username='bob', password='pass')
        self.client.login(username='alice', password='pass')

        # create top-level message and replies
        self.m1 = Message.objects.create(sender=self.alice, receiver=self.bob, content="Hello Bob")
        self.m1r1 = Message.objects.create(sender=self.bob, receiver=self.alice, content="Hi Alice", parent_message=self.m1)
        self.m1r1r1 = Message.objects.create(sender=self.alice, receiver=self.bob, content="How are you?", parent_message=self.m1r1)
        self.m2 = Message.objects.create(sender=self.alice, receiver=self.bob, content="Another top-level")

    def test_thread_with_returns_nested_structure(self):
        url = f"/api/messages/thread-with/{self.bob.id}/"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # Expect two top-level messages (m1, m2)
        top_ids = [m['id'] for m in data]
        self.assertIn(self.m1.id, top_ids)
        self.assertIn(self.m2.id, top_ids)
        # find m1 node and check replies nested
        m1_node = next((m for m in data if m['id'] == self.m1.id), None)
        self.assertIsNotNone(m1_node)
        # first reply should be m1r1
        self.assertTrue(len(m1_node['replies']) >= 1)
        self.assertEqual(m1_node['replies'][0]['id'], self.m1r1.id)
        # nested reply under m1r1
        nested = m1_node['replies'][0]['replies']
        self.assertTrue(len(nested) >= 1)
        self.assertEqual(nested[0]['id'], self.m1r1r1.id)

    def test_edit_creates_history_and_notif_on_create(self):
        # Create a new message and verify notification created for receiver
        msg = Message.objects.create(sender=self.alice, receiver=self.bob, content="Test notif")
        notif = Notification.objects.filter(user=self.bob, message=msg).exists()
        self.assertTrue(notif)

        # Edit message via patch (perform_update path)
        url = f"/api/messages/{msg.id}/"
        resp = self.client.patch(url, {"content": "Edited"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # History created
        histories = MessageHistory.objects.filter(message=msg)
        self.assertEqual(histories.count(), 1)
        self.assertEqual(histories.first().old_content, "Test notif")

    def test_delete_user_cleans_data(self):
        # login bob and delete account
        self.client.logout()
        self.client.login(username='bob', password='pass')
        resp = self.client.delete('/api/delete-account/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        # bob should be gone
        self.assertFalse(User.objects.filter(username='bob').exists())
        # messages where bob was receiver/sender should be removed
        self.assertEqual(Message.objects.filter(receiver__username='bob').count(), 0)
        self.assertEqual(Message.objects.filter(sender__username='bob').count(), 0)
        # any message histories edited_by bob should be removed
        self.assertEqual(MessageHistory.objects.filter(edited_by__username='bob').count(), 0)
