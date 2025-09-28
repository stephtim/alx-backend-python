#!/usr/bin/env python3
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from chats.models import Conversation, Message
from django.utils import timezone
from datetime import timedelta
import json


class EndToEndConversationMessageTests(TestCase):
    """
    End-to-end tests for conversations/messages including JWT auth.
    Covers:
      - JWT token obtain (login)
      - Creating a conversation
      - Sending messages (nested route)
      - Fetching conversations and messages
      - Access control: unauthorized users cannot see private conversations
    """

    def setUp(self):
        # Create two users
        self.alice = User.objects.create_user(username="alice", password="alicepass")
        self.bob = User.objects.create_user(username="bob", password="bobpass")
        self.charlie = User.objects.create_user(username="charlie", password="charliepass")

        # API clients
        self.client = APIClient()          # general client (unauthenticated by default)
        self.alice_client = APIClient()    # will hold JWT credentials for alice
        self.bob_client = APIClient()      # will hold JWT credentials for bob
        self.charlie_client = APIClient()  # charlie will remain either unauthorized or have his token for tests

        # Obtain and set JWT tokens for alice and bob
        alice_token = self.get_jwt_token_for_user(self.alice.username, "alicepass")
        bob_token = self.get_jwt_token_for_user(self.bob.username, "bobpass")
        charlie_token = self.get_jwt_token_for_user(self.charlie.username, "charliepass")

        self.alice_client.credentials(HTTP_AUTHORIZATION=f"Bearer {alice_token}")
        self.bob_client.credentials(HTTP_AUTHORIZATION=f"Bearer {bob_token}")
        self.charlie_client.credentials(HTTP_AUTHORIZATION=f"Bearer {charlie_token}")

    def get_jwt_token_for_user(self, username, password):
        """
        Helper that posts to the token endpoint and returns the access token string.
        Expects TokenObtainPairView available at /api/token/
        """
        resp = self.client.post(
            "/api/token/",
            data=json.dumps({"username": username, "password": password}),
            content_type="application/json",
        )
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_201_CREATED), msg=f"Token endpoint returned {resp.status_code} with body {resp.content}")
        data = resp.json()
        self.assertIn("access", data, msg=f"No access token in response: {data}")
        return data["access"]

    def test_create_conversation_send_messages_and_fetch(self):
        """
        alice creates a conversation with bob (alice is automatically a participant),
        alice and bob send messages, then alice fetches conversation and messages.
        """
        # 1) Alice creates a conversation
        create_conv_resp = self.alice_client.post(
            "/api/conversations/",
            data=json.dumps({"title": "Alice-Bob Chat"}),
            content_type="application/json",
        )
        self.assertEqual(create_conv_resp.status_code, status.HTTP_201_CREATED, msg=create_conv_resp.content)
        conv_data = create_conv_resp.json()
        conv_id = conv_data.get("id")
        self.assertIsNotNone(conv_id)

        # Ensure conversation participants include alice (perform_create in view should add)
        conv = Conversation.objects.get(id=conv_id)
        self.assertIn(self.alice, conv.participants.all())

        # Make Bob a participant as well (simulate adding bob)
        conv.participants.add(self.bob)
        conv.save()

        # 2) Alice posts a message to the nested messages endpoint
        alice_msg_resp = self.alice_client.post(
            f"/api/conversations/{conv_id}/messages/",
            data=json.dumps({"content": "Hello from Alice!"}),
            content_type="application/json",
        )
        self.assertEqual(alice_msg_resp.status_code, status.HTTP_201_CREATED, msg=alice_msg_resp.content)
        alice_msg = alice_msg_resp.json()
        self.assertEqual(alice_msg.get("content"), "Hello from Alice!")
        self.assertIn("sender", alice_msg)
        self.assertEqual(alice_msg["sender"]["username"], "alice")

        # 3) Bob posts a reply
        bob_msg_resp = self.bob_client.post(
            f"/api/conversations/{conv_id}/messages/",
            data=json.dumps({"content": "Hi Alice, Bob here."}),
            content_type="application/json",
        )
        self.assertEqual(bob_msg_resp.status_code, status.HTTP_201_CREATED, msg=bob_msg_resp.content)
        bob_msg = bob_msg_resp.json()
        self.assertEqual(bob_msg.get("content"), "Hi Alice, Bob here.")
        self.assertEqual(bob_msg["sender"]["username"], "bob")

        # 4) Alice fetches the conversation list and expects to see the conversation (and nested messages if serializer includes them)
        conv_list_resp = self.alice_client.get("/api/conversations/")
        self.assertEqual(conv_list_resp.status_code, status.HTTP_200_OK)
        convs = conv_list_resp.json()
        # convs might be a paginated response or a list depending on your view; handle both
        if isinstance(convs, dict) and "results" in convs:
            convs_items = convs["results"]
        else:
            convs_items = convs

        # Find our conversation in the returned list
        conv_ids = [c.get("id") for c in convs_items]
        self.assertIn(conv_id, conv_ids)

        # 5) Fetch nested messages (page 1)
        messages_resp = self.alice_client.get(f"/api/conversations/{conv_id}/messages/?page=1")
        self.assertEqual(messages_resp.status_code, status.HTTP_200_OK)
        messages_data = messages_resp.json()
        # Expect a paginated structure: keys 'count' and 'results' used in our pagination override
        self.assertIn("results", messages_data)
        results = messages_data["results"]
        # At least 2 messages (alice & bob)
        self.assertGreaterEqual(len(results), 2)
        # Verify messages content exist
        contents = [m["content"] for m in results]
        self.assertIn("Hello from Alice!", contents)
        self.assertIn("Hi Alice, Bob here.", contents)

    def test_unauthorized_cannot_access_private_conversation(self):
        """
        Create a conversation between alice and bob. Ensure charlie (not a participant)
        cannot view the conversation or post messages.
        """
        # Alice creates a conversation
        create_conv_resp = self.alice_client.post(
            "/api/conversations/",
            data=json.dumps({"title": "Private Alice-Bob Chat"}),
            content_type="application/json",
        )
        self.assertEqual(create_conv_resp.status_code, status.HTTP_201_CREATED)
        conv_id = create_conv_resp.json().get("id")
        conv = Conversation.objects.get(id=conv_id)
        # Add Bob as participant too
        conv.participants.add(self.bob)
        conv.save()

        # Charlie tries to GET the conversation list (should NOT include this private conv)
        charlie_conv_list = self.charlie_client.get("/api/conversations/")
        self.assertEqual(charlie_conv_list.status_code, status.HTTP_200_OK)
        body = charlie_conv_list.json()
        if isinstance(body, dict) and "results" in body:
            items = body["results"]
        else:
            items = body
        ids = [i.get("id") for i in items]
        self.assertNotIn(conv_id, ids, msg="Charlie should not see a conversation he is not a participant of")

        # Charlie attempts to GET nested messages for the conversation (should be 403 or 404 depending on permission handling)
        charlie_msgs = self.charlie_client.get(f"/api/conversations/{conv_id}/messages/")
        # Either forbidden (403) or empty result set / 404 depending on your view's behavior — we assert it's not 200 with data the charlie shouldn't see
        self.assertNotEqual(charlie_msgs.status_code, status.HTTP_200_OK, msg=f"Unauthorized user got 200: {charlie_msgs.content}")

        # Charlie attempts to POST a new message (should be 403)
        charlie_post = self.charlie_client.post(
            f"/api/conversations/{conv_id}/messages/",
            data=json.dumps({"content": "I should not be able to post"}),
            content_type="application/json",
        )
        self.assertIn(charlie_post.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND), msg=f"Unexpected status: {charlie_post.status_code}, body: {charlie_post.content}")

    def test_token_required_for_endpoints(self):
        """
        Ensure that endpoints require authentication (global DEFAULT_PERMISSION_CLASSES should be IsAuthenticated).
        Accessing endpoints with no credentials should result in 401.
        """
        # Unauthenticated client tries to list conversations
        resp = self.client.get("/api/conversations/")
        # Should be 401 Unauthorized (since global permission requires authentication)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
                      msg=f"Expected 401/403 for unauthenticated access but got {resp.status_code}, body {resp.content}")

        # Unauthenticated client tries to post to token endpoint with wrong creds should fail with 401/400
        bad_login = self.client.post("/api/token/", data=json.dumps({"username": "noone", "password": "bad"}), content_type="application/json")
        self.assertIn(bad_login.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_400_BAD_REQUEST))
