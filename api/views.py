from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from django.conf import settings

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.decorators import user_passes_test


from .models import *
from .serializers import *
from .forms import *
from .utils import *





@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def feedback_form_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                instance = form.save(commit=False)

                # Save feedback without an audio file
                instance.save()
                print(f"Feedback saved with id: {instance.id}")
                return redirect('feedback_list_create')
            except Exception as e:
                print(f"Error saving feedback: {str(e)}")
                return render(request, 'feedback_form.html', {'form': form, 'error': str(e)})
        else:
            print("Form validation failed.")
    else:
        form = FeedbackForm()

    return render(request, 'feedback_form.html', {'form': form})










class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    # permission_classes = [IsAdminUser]  

class MemberRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]  

class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminUser]  

    def perform_create(self, serializer):
        """Save feedback without audio."""
        try:
            instance = serializer.save()
            print(f"Feedback saved to database: {instance.id}")

            if 'audio_feedback' in self.request.FILES:
                audio_file = self.request.FILES['audio_feedback']
                print(f"Audio file received: {audio_file.name}")
                instance.audio_feedback = audio_file
                instance.save()
                print(f"Audio file saved: {instance.audio_feedback.name}")
            else:
                print("No audio file received.")

        except Exception as e:
            print(f"Error saving feedback: {str(e)}")
            raise

        return instance

class FeedbackRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminUser]  


class CheckMemberAPIView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]  

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')

        try:
            member = None
            if phone:
                member = Member.objects.get(phone=phone)

            if member:
                return Response({"message": "Member found", "member": MemberSerializer(member).data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

        except Member.DoesNotExist:
            return Response({"message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)


class CheckQRCodeView(APIView):
    permission_classes = [IsAdminUser]  

    def post(self, request, *args, **kwargs):
        serializer = CheckQRCodeSerializer(data=request.data)

        if serializer.is_valid():
            member_id = serializer.validated_data['id']

            try:
                member = Member.objects.get(id=member_id)
                return Response({"exists": True}, status=status.HTTP_200_OK)
            except Member.DoesNotExist:
                return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
