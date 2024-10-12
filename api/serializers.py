from rest_framework import serializers
from .models import *


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'company', 'position', 'phone', 'registration_time', 'qr_code']
        read_only_fields = ['registration_time', 'qr_code']



class FeedbackSerializer(serializers.ModelSerializer):
    member_data = MemberSerializer(source='member_id', read_only=True)
    class Meta:
        model = Feedback
        fields = ['id', 'feedback_body', 'member_data']


class CheckQRCodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()