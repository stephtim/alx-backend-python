#!/usr/bin/env python3
from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, create, update, or delete its messages.
    """

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level check:
        - If obj is a Message → check its conversation participants
        - If obj is a Conversation → check its participants
        """
        if hasattr(obj, "conversation"):  # Message instance
            return request.user in obj.conversation.participants.all()
        elif hasattr(obj, "participants"):  # Conversation instance
            return request.user in obj.participants.all()
        return False
