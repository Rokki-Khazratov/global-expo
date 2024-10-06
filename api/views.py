import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from django.conf import settings
from .models import *
from .serializers import *
from PIL import Image

class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class FeedbackRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer












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









class CheckQRCodeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CheckQRCodeSerializer(data=request.data)
        
        if serializer.is_valid():
            member_id = serializer.validated_data['id']
            
            try:
                # Проверка существования пользователя с указанным id
                member = Member.objects.get(id=member_id)
                return Response({"exists": True}, status=status.HTTP_200_OK)
            except Member.DoesNotExist:
                return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)
        
        # Если данные невалидны
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

