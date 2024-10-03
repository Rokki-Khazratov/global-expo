from rest_framework import serializers
from .models import *

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"

class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ['id', 'first_name', 'email', 'company', 'position', 'phone', 'registration_date', 'qr_code']
        read_only_fields = ['registration_date', 'qr_code']



class CheckQRCodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()