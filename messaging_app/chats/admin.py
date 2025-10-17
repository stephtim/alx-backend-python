<<<<<<< HEAD
# chats/admin.py
=======
>>>>>>> 6e94a15ad0e04ccb334ae164477d76e6f22c87ac
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Conversation, Message, MessageHistory

# --------------------------
# User model
# --------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_staff', 'is_superuser')
    ordering = ('email',)

# --------------------------
# Conversation model
# --------------------------
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')

<<<<<<< HEAD
# --------------------------
# Message model
# --------------------------
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp', 'parent_message', 'edited', 'edit_count')
    search_fields = ('content',)
=======
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'timestamp')
>>>>>>> 6e94a15ad0e04ccb334ae164477d76e6f22c87ac

# --------------------------
# MessageHistory model
# --------------------------
@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'version', 'edited_by', 'edited_at')
<<<<<<< HEAD
    search_fields = ('message__content',)
=======
>>>>>>> 6e94a15ad0e04ccb334ae164477d76e6f22c87ac
