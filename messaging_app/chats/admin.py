# chats/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Conversation, Message, MessageHistory

# --------------------------
# User model
# --------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "role", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    readonly_fields = ("password_hash",)

# --------------------------
# Conversation model
# --------------------------
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("conversation_id", "created_at")
    filter_horizontal = ("participants",)

# --------------------------
# Message model
# --------------------------
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp', 'parent_message', 'edited', 'edit_count')
    search_fields = ('content',)

# --------------------------
# MessageHistory model
# --------------------------
@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'version', 'edited_by', 'edited_at')
    search_fields = ('message__content',)
