#!/usr/bin/env python3
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message, Notification
from .serializers import MessageSerializer, NotificationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Example: show only messages received by the authenticated user
        return Message.objects.filter(receiver=self.request.user).select_related('sender', 'receiver')

    def perform_create(self, serializer):
        # Ensure sender is always the authenticated user
        serializer.save(sender=self.request.user, receiver=self.request.data.get('receiver'))


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


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
