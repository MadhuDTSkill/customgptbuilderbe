from django.urls import path
from .views import  CustomGPTAssistChatView, CustomGPTAssistJsonDataChatView


urlpatterns = [
    path('assist/', CustomGPTAssistChatView.as_view(), name='custom_gpt_assist_chat'),
    path('assist/json_data/', CustomGPTAssistJsonDataChatView.as_view(), name='custom_gpt_assist_json_data_chat'),
]
