
# Create your views here.
# chats/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        # This is where you implement the logic to create a new message
        # and associate it with a conversation.
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")
        sender = request.user  # Assuming a logged-in user

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND
            )

        message = Message.objects.create(
            conversation=conversation, sender=sender, message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated] # pyright: ignore[reportUndefinedVariable]

    def get_queryset(self):
        """
        Only show conversations where the logged-in user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """
        Add the creator as a participant automatically.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        List messages only from conversations the user participates in.
        """
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign sender as the logged-in user.
        The conversation must already exist.
        """
        conversation_id = self.request.data.get("conversation_id")
        conversation = Conversation.objects.get(conversation_id=conversation_id)

        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise PermissionError("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=["get"]) # pyright: ignore[reportUndefinedVariable]
    def messages(self, request, pk=None):
        """
        GET /api/conversations/{id}/messages/
        """
        conversation = self.get_object()
        messages = Message.objects.filter(conversation=conversation)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
