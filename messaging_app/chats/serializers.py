# chats/serializers.py
#!/usr/bin/env python3
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # Example: explicitly include username with CharField
    username = serializers.CharField(required=True, max_length=150)

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    # Example: custom formatting of timestamp using SerializerMethodField
    sent_at_human = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'sent_at', 'sent_at_human']

    def get_sent_at_human(self, obj):
        # human-friendly representation of timestamp
        return obj.sent_at.strftime("%Y-%m-%d %H:%M:%S")

    def validate_content(self, value):
        # Example validation using ValidationError
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'participants', 'messages']

class MessageHistorySerializer(serializers.ModelSerializer):
    edited_by = serializers.StringRelatedField()  # or use a UserSerializer

    class Meta:
        model = MessageHistory
        fields = ('id', 'version', 'old_content', 'edited_by', 'edited_at')