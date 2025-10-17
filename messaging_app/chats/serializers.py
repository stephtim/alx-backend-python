from rest_framework import serializers
<<<<<<< HEAD
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from .models import User, Conversation, Message, MessageHistory

=======
from .models import User, Conversation, Message, MessageHistory
>>>>>>> 6e94a15ad0e04ccb334ae164477d76e6f22c87ac

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

<<<<<<< HEAD
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
=======
class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = '__all__'
>>>>>>> 6e94a15ad0e04ccb334ae164477d76e6f22c87ac
