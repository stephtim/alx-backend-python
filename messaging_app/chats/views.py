#!/usr/bin/env python3
from rest_framework import viewsets, permissions, status, filters as drf_filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .models import Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter, ConversationFilter
from .pagination import MessagePagination  # optional; global PAGE_SIZE also works


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ['title', 'participants__username']
    ordering_fields = ['id']

    def get_queryset(self):
        # Only conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    # Filtering, searching and ordering
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['content', 'sender__username']
    ordering_fields = ['sent_at', 'id']
    # Pagination: will use global PageNumberPagination (PAGE_SIZE=20). 
    # To explicitly use the local paginator, uncomment the line below:
    pagination_class = MessagePagination

    def get_queryset(self):
        """
        If nested route /conversations/{conversation_id}/messages/ is used,
        filter to that conversation after verifying the user is a participant.
        Otherwise filter messages to conversations the user participates in.
        """
        qs = Message.objects.all()
        conversation_id = self.kwargs.get("conversation_id")

        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                return Message.objects.none()

            # ensure the requester is a conversation participant
            if self.request.user not in conversation.participants.all():
                raise PermissionDenied(detail="You are not a participant of this conversation.")

            qs = qs.filter(conversation=conversation)

        # always narrow down to messages in conversations the user participates in
        return qs.filter(conversation__participants=self.request.user).distinct()

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_id")
        if not conversation_id:
            raise PermissionDenied(detail="Conversation id is required to create a message.", code=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied(detail="Conversation does not exist.", code=status.HTTP_404_NOT_FOUND)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant of this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
