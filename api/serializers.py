from rest_framework import serializers
from .models import *


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'email', 'company', 'position', 'phone', 'registration_date', 'qr_code']
        read_only_fields = ['registration_date', 'qr_code']


class FeedbackSerializer(serializers.ModelSerializer):
    member_data = MemberSerializer(source='member_id', read_only=True)  # Use source to point to the related field
    class Meta:
        model = Feedback
        fields = ['id','feedback_body','member_data','audio_feedback']


class CheckQRCodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()