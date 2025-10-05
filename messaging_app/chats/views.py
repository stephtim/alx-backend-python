#!/usr/bin/env python3

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Message, Notification
from .serializers import MessageSerializer, MessageHistorySerializer


class IsParticipant(permissions.BasePermission):
    """
    Custom permission: only allow participants (sender or receiver) to view a message.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user


class MessageViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for messages.
    - List messages for current user
    - Create new messages
    - Update message content (edits trigger pre_save signal)
    - Retrieve message history
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

    def get_queryset(self):
        user = self.request.user
        # user can see messages they sent or received
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

    def perform_update(self, serializer):
        """
        Called before saving a message update.
        Sets _editor so the pre_save signal can log the old content and who edited.
        """
        instance = serializer.instance

        # Only the sender can edit
        if self.request.user != instance.sender:
            raise PermissionDenied("You are not allowed to edit this message.")

        # Step 6: attach editor info so signal can use it
        serializer.instance._editor = self.request.user

        # Saving triggers pre_save signal → MessageHistory entry created
        serializer.save()

    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, pk=None):
        """
        GET /api/messages/<id>/history/
        Returns all previous versions of the message.
        """
        message = self.get_object()
        histories = message.histories.order_by('-version')
        serializer = MessageHistorySerializer(histories, many=True)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer # type: ignore


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def delete_user(request):
    """
    DELETE /api/delete-account/
    Deletes the authenticated user and triggers cleanup.
    """
    user = request.user
    user.delete()
    return Response({"detail": "Account and related data deleted."}, status=status.HTTP_204_NO_CONTENT)