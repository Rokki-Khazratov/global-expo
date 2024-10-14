from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from django.conf import settings

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum



from .models import *
from .serializers import *
from .forms import *
from .utils import *


@user_passes_test(lambda u: u.is_superuser)
def bank_list_view(request):
    # Annotate each bank with the total points and order them by points in descending order
    banks = Bank.objects.annotate(total_points=Sum('feedback__stars')).order_by('-total_points')

    # Debugging: Print each bank and its total points
    for bank in banks:
        print(f"{bank.name}: {bank.total_points or 0} points")

    return render(request, 'bank_list.html', {'banks': banks})




# @user_passes_test(lambda u: u.is_superuser)
# def feedback_form_view(request):
#     if request.method == 'POST':
#         try:
#             member_id = request.POST.get('member_id')
#             bank_id = request.POST.get('bank')
#             feedback_body = request.POST.get('feedback_body')
#             stars = request.POST.get('stars')

#             # Print values for debugging
#             print(f"Member ID: {member_id}, Bank ID: {bank_id}, Stars: {stars}")

#             if not stars or not member_id or not bank_id:
#                 raise ValueError("Invalid data: All fields are required.")

#             # Save feedback
#             feedback = Feedback.objects.create(
#                 member_id_id=member_id,
#                 bank_id=bank_id,
#                 feedback_body=feedback_body,
#                 stars=int(stars)  # Ensure stars is saved as an integer
#             )

#             print(f"Feedback saved: {feedback}")
#             return redirect('feedback_form')

#         except Exception as e:
#             print(f"Error occurred: {e}")
#             return render(request, 'feedback-form.html', {
#                 'error_message': 'Произошла ошибка при отправке. Пожалуйста, попробуйте снова.',
#                 'members': Member.objects.all(),
#                 'banks': Bank.objects.all()
#             })

#     members = Member.objects.all()
#     banks = Bank.objects.all()
#     return render(request, 'feedback-form.html', {'members': members, 'banks': banks})




# api/views.py
    
@user_passes_test(lambda u: u.is_superuser)
def feedback_form_view(request):
    if request.method == 'POST':
        try:
            member_id = request.POST.get('member_id')
            bank_id = request.POST.get('bank')
            feedback_body = request.POST.get('feedback_body')
            stars = request.POST.get('stars')
            voter_id = request.user.username  # Use the voter's username or another unique ID

            # Check if the voter has already voted for this bank
            if Feedback.objects.filter(voter_id=voter_id, bank_id=bank_id).exists():
                raise ValueError("Вы уже голосовали за этот банк.")

            # Save the feedback if not already voted
            feedback = Feedback.objects.create(
                member_id_id=member_id,
                bank_id=bank_id,
                feedback_body=feedback_body,
                stars=int(stars),
                voter_id=voter_id
            )

            print(f"Feedback saved: {feedback}")
            return redirect('feedback_form')

        except ValueError as ve:
            print(f"Validation error: {ve}")
            return render(request, 'feedback-form.html', {
                'error_message': str(ve),
                'members': Member.objects.all(),
                'banks': Bank.objects.all()
            })
        except Exception as e:
            print(f"Error occurred: {e}")
            return render(request, 'feedback-form.html', {
                'error_message': 'Произошла ошибка при отправке. Пожалуйста, попробуйте снова.',
                'members': Member.objects.all(),
                'banks': Bank.objects.all()
            })

    # GET request: render the form with participants and banks
    return render(request, 'feedback-form.html', {
        'members': Member.objects.all(),
        'banks': Bank.objects.all()
    })











class MemberCreateView(generics.CreateAPIView):
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


