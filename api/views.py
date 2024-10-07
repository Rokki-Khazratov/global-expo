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
    parser_classes = (MultiPartParser, FormParser)  # Для загрузки файлов

    def perform_create(self, serializer):
        """Переопределяем сохранение, чтобы работать с аудиофайлами."""
        try:
            # Сохраняем экземпляр Feedback
            instance = serializer.save()
            print(f"Отзыв сохранен в базе данных: {instance.id}")

            # Проверяем, был ли загружен аудиофайл
            if 'audio_feedback' in self.request.FILES:
                audio_file = self.request.FILES['audio_feedback']
                print(f"Аудиофайл получен: {audio_file.name}")

                # Сохраняем аудиофайл напрямую в модель 
                instance.audio_feedback = audio_file
                instance.save()

                print(f"Аудиофайл сохранен в базе данных: {instance.audio_feedback.name}")
            else:
                print("Аудиофайл не был получен.")
        
        except Exception as e:
            print(f"Ошибка при создании отзыва: {str(e)}")
            raise

        return instance

class FeedbackRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer




#!wav to mp3
# def feedback_form_view(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST, request.FILES)  # request.FILES обязательно для файлов
#         if form.is_valid():
#             try:
#                 instance = form.save(commit=False)

#                 # Логирование файла
#                 if 'audio_feedback' in request.FILES:
#                     audio_file = request.FILES['audio_feedback']
#                     print(f"Аудиофайл получен: {audio_file.name}, размер: {audio_file.size}")

#                     # Пробуем сохранить файл
#                     output_filename = save_audio_as_mp3(audio_file, instance)
#                     print(f"Аудиофайл конвертирован в MP3 и сохранен как: {output_filename}")
#                     instance.audio_feedback.name = f'audio_feedbacks/{output_filename}'
#                 else:
#                     print('AUdifile ne poluchen')

#                 instance.save()
#                 print(f"Отзыв сохранен в базе данных с id: {instance.id}")
#                 return redirect('feedback_list_create')
#             except Exception as e:
#                 print(f"Ошибка при сохранении отзыва: {str(e)}")
#                 return render(request, 'feedback_form.html', {'form': form, 'error': str(e)})
#         else:
#             print("Форма не прошла валидацию.")
#     else:
#         form = FeedbackForm()

#     return render(request, 'feedback_form.html', {'form': form})

#!WAV
def feedback_form_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)  # request.FILES обязательно для файлов
        if form.is_valid():
            try:
                instance = form.save(commit=False)

                # Проверяем наличие файла в запросе
                if 'audio_feedback' in request.FILES:
                    audio_file = request.FILES['audio_feedback']
                    print(f"Аудиофайл получен: {audio_file.name}, размер: {audio_file.size}")

                    # Сохраняем аудиофайл напрямую в базу данных
                    instance.audio_feedback = audio_file
                else:
                    print('Аудиофайл не получен')

                # Сохраняем отзыв с аудиофайлом
                instance.save()
                print(f"Отзыв сохранен в базе данных с id: {instance.id}")
                return redirect('feedback_list_create')
            except Exception as e:
                print(f"Ошибка при сохранении отзыва: {str(e)}")
                return render(request, 'feedback_form.html', {'form': form, 'error': str(e)})
        else:
            print("Форма не прошла валидацию.")
    else:
        form = FeedbackForm()

    return render(request, 'feedback_form.html', {'form': form})

#!member qr maker with role if exhibitor





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
    

