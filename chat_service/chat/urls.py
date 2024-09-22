from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomGPTViewSet, CustomGPTLiteListView, ChatView, MessagesListView

router = DefaultRouter()
router.register(r'gpts', CustomGPTViewSet, basename='gpts')

urlpatterns = [
    path('', include(router.urls)),
    path('gpts/lite-list', CustomGPTLiteListView.as_view()),
    path('messages/<str:gpt_id>', MessagesListView.as_view()),
    path('<str:gpt_id>', ChatView.as_view()),
]
