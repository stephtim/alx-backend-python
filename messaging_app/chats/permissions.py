#!/usr/bin/env python3
#!/usr/bin/env python3
from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API
    - Only participants of a conversation can view, send, update, or delete messages
    """

    def has_permission(self, request, view):
        # User must be authenticated for any action
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level checks:
        - GET: participants can view
        - POST: participants can send
        - PUT/PATCH/DELETE: participants can update or delete
        """
        user = request.user

        # Check if obj is a Message → verify its conversation participants
        if hasattr(obj, "conversation"):
            participants = obj.conversation.participants.all()
        # Check if obj is a Conversation → verify participants directly
        elif hasattr(obj, "participants"):
            participants = obj.participants.all()
        else:
            return False

        # Allow only participants to do anything
        if user not in participants:
            return False

        # Allow safe methods (GET, HEAD, OPTIONS) by default
        if request.method in permissions.SAFE_METHODS:
            return True

        # Explicitly allow PUT, PATCH, DELETE for participants
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return True

        # Default allow POST for participants
        if request.method == "POST":
            return True

        return False
