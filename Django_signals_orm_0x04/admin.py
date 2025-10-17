# chats/admin.py
from django.contrib import admin
from .models import Message, MessageHistory, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp')
    ordering = ('-timestamp',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'actor', 'verb', 'is_read', 'created_at')
    list_filter = ('is_read',)
    ordering = ('-created_at',)

lass MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    readonly_fields = ('version', 'old_content', 'edited_by', 'edited_at')
    extra = 0

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp', 'edited', 'edit_count')
    inlines = [MessageHistoryInline]

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'version', 'edited_by', 'edited_at')
    readonly_fields = ('old_content',)