from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Member, Ticket
from .serializers import MemberSerializer, TicketSerializer

class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class CheckTicketAPIView(generics.GenericAPIView):
    serializer_class = TicketSerializer

    def post(self, request, *args, **kwargs):
        ticket_id = request.data.get('ticket_id')
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            if ticket.is_valid:
                return Response({"message": "Билет действителен", "member": MemberSerializer(ticket.member).data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Билет недействителен"}, status=status.HTTP_400_BAD_REQUEST)
        except Ticket.DoesNotExist:
            return Response({"message": "Билет не найден"}, status=status.HTTP_404_NOT_FOUND)

class CheckMemberAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        phone = request.data.get('phone')

        try:
            member = None
            if email:
                member = Member.objects.get(email=email)
            elif phone:
                member = Member.objects.get(phone=phone)
            
            if member:
                return Response({"message": "Участник найден", "member": MemberSerializer(member).data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Участник не найден"}, status=status.HTTP_404_NOT_FOUND)

        except Member.DoesNotExist:
            return Response({"message": "Участник не найден"}, status=status.HTTP_404_NOT_FOUND)
