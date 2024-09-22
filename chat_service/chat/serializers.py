from rest_framework import serializers
from .models import CustomGPT, Message

class CustomGPTSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = CustomGPT
        fields = ['id', 'name', 'short_description', 'system_prompt', 'user_id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M %p')  

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M %p')  

class CustomGPTSerializerLite(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = CustomGPT
        fields = ['id', 'name', 'short_description', 'user_id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M %p')  

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M %p')  


class ChatSerializer(serializers.Serializer):
    input = serializers.CharField()
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'custom_gpt', 'user_id', 'user_message', 'ai_message', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']