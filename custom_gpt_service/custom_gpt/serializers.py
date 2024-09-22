from rest_framework import serializers


class CustomGPTChatSerializer(serializers.Serializer):
    input = serializers.CharField()
    
class CustomGPTJsonDataChatSerializer(serializers.Serializer):
    name = serializers.CharField()
    short_description = serializers.CharField()
    system_prompt = serializers.CharField()
    user_message = serializers.CharField()
    assistant_response = serializers.CharField()
    