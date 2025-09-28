#!/usr/bin/env python3
from django_filters import rest_framework as filters
from .models import Message, Conversation


class MessageFilter(filters.FilterSet):
    """
    Filters for Message list endpoints (top-level or nested under a conversation).
    Query params:
      - conversation_id       : exact conversation id
      - participant_id        : id of a conversation participant (messages in conversations that include this user)
      - sender_id             : id of the message sender
      - sender_username       : partial match on sender username
      - start                 : ISO8601 datetime for sent_at >= start
      - end                   : ISO8601 datetime for sent_at <= end
      - content               : partial match in message content
    """
    conversation_id = filters.NumberFilter(field_name='conversation__id', lookup_expr='exact')
    participant_id = filters.NumberFilter(method='filter_by_participant')
    sender_id = filters.NumberFilter(field_name='sender__id', lookup_expr='exact')
    sender_username = filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    start = filters.IsoDateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end = filters.IsoDateTimeFilter(field_name='sent_at', lookup_expr='lte')
    content = filters.CharFilter(field_name='content', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['conversation_id', 'participant_id', 'sender_id', 'sender_username', 'start', 'end', 'content']

    def filter_by_participant(self, queryset, name, value):
        # messages in conversations where the participant (user) with id=value is present
        return queryset.filter(conversation__participants__id=value).distinct()


class ConversationFilter(filters.FilterSet):
    """
    Filters for Conversation list endpoints.
    Query params:
      - participant_id : filter conversations that include this user id
      - participant_username : partial username match
    """
    participant_id = filters.NumberFilter(method='filter_by_participant')
    participant_username = filters.CharFilter(method='filter_by_participant_username')

    class Meta:
        model = Conversation
        fields = ['participant_id', 'participant_username']

    def filter_by_participant(self, queryset, name, value):
        return queryset.filter(participants__id=value).distinct()

    def filter_by_participant_username(self, queryset, name, value):
        return queryset.filter(participants__username__icontains=value).distinct()
