# chats/apps.py
from django.apps import AppConfig


class ChatsConfig(AppConfig):
    name = 'chats'
    verbose_name = 'Chats'

    def ready(self):
        # import signals so receivers are registered
        import chats.signals  # noqa: F401
