from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from django.conf import settings
from .models import *
from .serializers import *
from .forms import *
from .utils import *






class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer



class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    parser_classes = (MultiPartParser, FormParser)  # Убедись, что используются правильные парсеры для файлов

    def perform_create(self, serializer):
        """Переопределяем сохранение, чтобы работать с аудиофайлами."""
        instance = serializer.save()

        # Если есть аудиофайл, обработаем его
        if self.request.FILES.get('audio_feedback'):
            audio_file = self.request.FILES['audio_feedback']
            output_filename = save_audio_as_mp3(audio_file, instance)  # Конвертируем и сохраняем как MP3

            # Сохраняем имя файла в модели
            instance.audio_feedback.name = f'audio_feedbacks/{output_filename}'
            instance.save()

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
    

