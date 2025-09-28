
# Create your views here.
# chats/views.py
#!/usr/bin/env python3
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically include the requesting user as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure sender is always the logged-in user
        serializer.save(sender=self.request.user)
