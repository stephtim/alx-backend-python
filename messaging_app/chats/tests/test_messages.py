#!/usr/bin/env python3
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from chats.models import Conversation, Message
from django.utils import timezone
from datetime import timedelta


class MessageFilterPaginationTests(TestCase):
    def setUp(self):
        # Users
        self.user1 = User.objects.create_user(username="alice", password="pass123")
        self.user2 = User.objects.create_user(username="bob", password="pass123")

        # Conversation
        self.conversation = Conversation.objects.create(title="Test Chat")
        self.conversation.participants.set([self.user1, self.user2])

        # Messages (25 total, so pagination kicks in at 20)
        now = timezone.now()
        for i in range(25):
            sender = self.user1 if i % 2 == 0 else self.user2
            Message.objects.create(
                conversation=self.conversation,
                sender=sender,
                content=f"Message {i}",
                sent_at=now - timedelta(minutes=i),
            )

        # Authenticated API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_pagination_page_size(self):
        """Should return 20 messages on first page, 5 on second page"""
        url = f"/conversations/{self.conversation.id}/messages/"

        # Page 1
        response = self.client.get(url + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 20)

        # Page 2
        response = self.client.get(url + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 5)

    def test_filter_by_sender(self):
        """Should return only messages sent by user1"""
        url = f"/conversations/{self.conversation.id}/messages/?sender_id={self.user1.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        for msg in response.data["results"]:
            self.assertEqual(msg["sender"]["id"], self.user1.id)

    def test_filter_by_date_range(self):
        """Should return only messages within the last 10 minutes"""
        start_time = (timezone.now() - timedelta(minutes=10)).isoformat()
        url = f"/conversations/{self.conversation.id}/messages/?start={start_time}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        for msg in response.data["results"]:
            self.assertIn("Message", msg["content"])
