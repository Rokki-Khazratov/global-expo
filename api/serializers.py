from rest_framework import serializers
from .models import Member, Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['ticket_id', 'is_valid']

class MemberSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'email', 'company', 'position', 'phone', 'registration_date', 'tickets']
        read_only_fields = ['registration_date']
