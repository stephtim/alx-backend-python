# chats/models.py
#!/usr/bin/env python3
# messaging/models.py

"""
This is the project-level models.py file.
It intentionally does not define models, because all actual models
(e.g., Message, Notification, MessageHistory) are defined inside the `chats` app.
"""

from django.db import models  # ✅ Required for Django's model discovery mechanism
# For reference: Message model (with unread manager) is defined in chats/models.py
from chats.models import Message  # Message includes parent_message and unread manager

# No models are defined here.
# All models are located in chats/models.py and imported where needed.
