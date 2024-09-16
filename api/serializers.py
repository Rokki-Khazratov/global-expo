from rest_framework import serializers
from .models import Member, Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['ticket_id', 'is_valid', 'qr_code']

class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ['id', 'first_name', 'email', 'company', 'position', 'phone', 'registration_date', 'qr_code']
        read_only_fields = ['registration_date', 'qr_code']



class CheckQRCodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()