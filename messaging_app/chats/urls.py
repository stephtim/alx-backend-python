# messaging_app/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet)
router.register(r"messages", MessageViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
