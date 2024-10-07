from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from django.conf import settings

import logging
from .models import *
from .serializers import *
from .forms import *
from .utils import *





logger = logging.getLogger(__name__)


class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer





class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    parser_classes = (MultiPartParser, FormParser)  # Парсеры для работы с файлами

    def perform_create(self, serializer):
        """Переопределяем сохранение, чтобы работать с аудиофайлами."""
        try:
            # Сохраняем экземпляр Feedback
            instance = serializer.save()
            logger.info(f"Отзыв сохранен в базе данных: {instance.id}")

            # Проверяем, был ли загружен аудиофайл
            if 'audio_feedback' in self.request.FILES:
                audio_file = self.request.FILES['audio_feedback']
                logger.info(f"Аудиофайл получен: {audio_file.name}")

                # Сохраняем аудиофайл напрямую в модель
                instance.audio_feedback = audio_file
                instance.save()

                logger.info(f"Аудиофайл сохранен в базе данных: {instance.audio_feedback.name}")
            else:
                logger.warning("Аудиофайл не был получен.")
        
        except Exception as e:
            logger.error(f"Ошибка при создании отзыва: {str(e)}")
            raise

        return instance

class FeedbackRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer





def feedback_form_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_list_create')  # Redirect after successful submission to the API view
    else:
        form = FeedbackForm()

    return render(request, 'feedback_form.html', {'form': form})








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
    

