#!/usr/bin/env python3
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Message, Notification
from .serializers import MessageSerializer, NotificationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        """
        Cache the list view for 60 seconds.
        """
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        # Example: show only messages received by the authenticated user
        return Message.objects.filter(receiver=self.request.user).select_related('sender', 'receiver')

    def perform_create(self, serializer):
        # Ensure sender is always the authenticated user
        serializer.save(sender=self.request.user, receiver=self.request.data.get('receiver'))

    @action(detail=False, methods=['get'], url_path='unread')
    def unread_messages(self, request):
        # Use the custom manager to get unread messages for the user, optimized with .only()
        unread_qs = Message.unread.for_user(request.user).only('id', 'content', 'timestamp', 'sender_id', 'receiver_id')
        serializer = self.get_serializer(unread_qs, many=True)
        return Response(serializer.data)


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
