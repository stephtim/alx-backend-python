#!/usr/bin/env python3

#!/usr/bin/env python3
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

from django.db.models import Q, Prefetch

from chats.models import Message, MessageHistory, Notification
from .serializers import (
    MessageSerializer, ThreadedMessageSerializer, MessageHistorySerializer,
    UserSimpleSerializer
)

def home(request):
    return render(request, 'index.html')

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related('sender', 'receiver', 'parent_message')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # default: messages user sent or received
        return Message.objects.filter(Q(sender=user) | Q(receiver=user)).select_related('sender','receiver','parent_message')

    def perform_create(self, serializer):
        # attach sender automatically
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        # only sender allowed to edit
        if self.request.user != instance.sender:
            raise PermissionDenied("Only sender can edit the message.")
        # attach editor for signal to capture
        serializer.instance._editor = self.request.user
        serializer.save()

    @action(detail=False, methods=['get'], url_path='thread-with/(?P<other_user_id>[^/.]+)')
    def thread_with(self, request, other_user_id=None):
        """
        GET /api/messages/thread-with/<other_user_id>/
        Returns a threaded view of messages between request.user and other_user_id.
        - Fetches all messages between the two users with select_related/prefetch to avoid N+1.
        - Builds the reply tree in-memory and returns nested JSON.
        """
        user = request.user
        try:
            other_id = int(other_user_id)
        except (ValueError, TypeError):
            return Response({"detail": "Invalid user id"}, status=status.HTTP_400_BAD_REQUEST)

        base_q = Message.objects.filter(
            (Q(sender_id=user.id) & Q(receiver_id=other_id)) |
            (Q(sender_id=other_id) & Q(receiver_id=user.id))
        ).select_related('sender', 'receiver', 'parent_message').order_by('timestamp')

        # prefetch histories for convenience (not required for threading)
        base_q = base_q.prefetch_related(Prefetch('histories', queryset=MessageHistory.objects.select_related('edited_by')))

        messages = list(base_q)

        # Build mapping id -> node and children lists
        nodes = {}
        children_map = {}
        for m in messages:
            nodes[m.id] = {
                'id': m.id,
                'sender': {'id': m.sender.id, 'username': m.sender.username},
                'receiver': {'id': m.receiver.id, 'username': m.receiver.username},
                'content': m.content,
                'timestamp': m.timestamp,
                'parent_message': m.parent_message_id,
                'edited': m.edited,
                'edit_count': m.edit_count,
                'replies': []
            }
            children_map.setdefault(m.parent_message_id, []).append(m.id)

        # recursively attach children — iterative approach avoids recursion limits
        def build_tree(root_ids):
            result = []
            stack = list(root_ids)[::-1]  # process in timestamp order (since messages ordered)
            while stack:
                msg_id = stack.pop()
                node = nodes[msg_id]
                # attach children
                child_ids = children_map.get(msg_id, [])
                # ensure children are sorted by timestamp (they are from base_q order)
                node['replies'] = [nodes[cid] for cid in child_ids]
                # push children onto stack to ensure their replies are processed
                for cid in reversed(child_ids):
                    stack.append(cid)
                result.append(node)
            return result

        # root messages are those with parent_message = None
        root_ids = [m.id for m in messages if m.parent_message_id is None]
        threaded = build_tree(root_ids)

        # Validate / serialize with ThreadedMessageSerializer
        serializer = ThreadedMessageSerializer(threaded, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, pk=None):
        msg = self.get_object()
        histories = msg.histories.select_related('edited_by').order_by('-version')
        serializer = MessageHistorySerializer(histories, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"detail": "Account and related data deleted."}, status=status.HTTP_204_NO_CONTENT)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer