#!/usr/bin/env python3
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message, Notification
from .serializers import MessageSerializer, NotificationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


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
