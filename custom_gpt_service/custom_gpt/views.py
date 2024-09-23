from rest_framework import views
from rest_framework.response import Response
from .permissions import IsUserIDAuthenticated
from .serializers import CustomGPTChatSerializer, CustomGPTJsonDataChatSerializer, CustomGPTTestChatSerializer
from utils.chat import Chat

class CustomGPTAssistChatView(views.APIView):
    permission_classes = [IsUserIDAuthenticated]
    serializer_class = CustomGPTChatSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.request.user
        chat = Chat(user_id)
        response = chat.get_response(serializer.validated_data)
        return Response({"input" : serializer.validated_data, 'response': response})

class CustomGPTAssistJsonDataChatView(views.APIView):
    permission_classes = [IsUserIDAuthenticated]
    serializer_class = CustomGPTJsonDataChatSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.request.user
        chat = Chat(user_id, False)
        response = chat.get_response(serializer.validated_data)
        return Response({"input" : serializer.validated_data,'response': response})

class CustomGPTTestChatView(views.APIView):
    permission_classes = [IsUserIDAuthenticated]
    serializer_class = CustomGPTTestChatSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.request.user
        chat = Chat(user_id, True, serializer.validated_data['system_prompt'])
        response = chat.get_response(serializer.validated_data)
        return Response({"input" : serializer.validated_data,'response': response})

