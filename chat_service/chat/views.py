from rest_framework import viewsets, generics, views
from rest_framework.response import Response
from .models import CustomGPT, Message
from .serializers import CustomGPTSerializer, CustomGPTSerializerLite, ChatSerializer, MessageSerializer
from .permissions import IsUserIDAuthenticated
from utils.chat import Chat


class CustomGPTViewSet(viewsets.ModelViewSet):
    queryset = CustomGPT.objects.all()
    serializer_class = CustomGPTSerializer
    permission_classes = [IsUserIDAuthenticated]


class CustomGPTLiteListView(generics.ListAPIView):
    queryset = CustomGPT.objects.all()
    serializer_class = CustomGPTSerializerLite
    permission_classes = [IsUserIDAuthenticated]


class ChatView(views.APIView):
    queryset = CustomGPT.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsUserIDAuthenticated]


    def post(self, request, gpt_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        input = serializer.validated_data['input']
        gpt = self.queryset.get(id=gpt_id)        
        chat = Chat(gpt, user_id=request.user)
        response = chat.get_response(input)
        return Response({'input' : input, 'response': response})


class MessagesListView(views.APIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsUserIDAuthenticated]
    
    def get(self, request, gpt_id):
        messages = self.queryset.filter(custom_gpt_id=gpt_id, user_id = request.user)
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data)