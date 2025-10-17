# chats/serializers.py
#!/usr/bin/env python3
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from .models import User, Conversation, Message, MessageHistory


User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class MessageHistorySerializer(serializers.ModelSerializer):
    edited_by = UserSimpleSerializer()
    class Meta:
        model = MessageHistory
        fields = ('id', 'version', 'old_content', 'edited_by', 'edited_at')

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSimpleSerializer(read_only=True)
    receiver = UserSimpleSerializer(read_only=True)
    parent_message = serializers.PrimaryKeyRelatedField(read_only=True)
    edit_count = serializers.IntegerField(read_only=True)
    edited = serializers.BooleanField(read_only=True)
    edited_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'content', 'timestamp',
                  'parent_message', 'edited', 'edited_at', 'edit_count')

class ThreadedMessageSerializer(serializers.Serializer):
    """
    Light-weight serializer for threaded responses. Expects dicts produced by the view.
    """
    id = serializers.IntegerField()
    sender = UserSimpleSerializer()
    receiver = UserSimpleSerializer()
    content = serializers.CharField()
    timestamp = serializers.DateTimeField()
    parent_message = serializers.IntegerField(allow_null=True)
    edited = serializers.BooleanField()
    edit_count = serializers.IntegerField()
    replies = serializers.ListField(child=serializers.DictField(), default=[])

    class ConversationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Conversation
            fields = "__all__"