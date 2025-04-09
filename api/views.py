from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from django.conf import settings
from django.http import JsonResponse

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum



from .models import *
from .serializers import *
from .forms import *
from .utils import *


@user_passes_test(lambda u: u.is_superuser)
def company_list_view(request):
    # Annotate each company with the total points and order them by points in descending order
    companies = Company.objects.annotate(total_points=Sum('feedback__stars')).order_by('-total_points')
    
    # Debugging: Print each company and its total points
    for company in companies:
        print(f"{company.name}: {company.total_points or 0} points")
    
    return render(request, 'company_list.html', {'companies': companies})




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
def feedback_form(request):
    if request.method == 'POST':
        member_id = request.POST.get('member')
        company_id = request.POST.get('company')
        stars = request.POST.get('stars')
        
        if not stars or not member_id or not company_id:
            return JsonResponse({'error': 'Все поля обязательны'}, status=400)
        
        try:
            feedback = Feedback.objects.create(
                member_id_id=member_id,
                company_id=company_id,
                stars=stars
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    members = Member.objects.all()
    companies = Company.objects.all()
    return render(request, 'feedback-form.html', {
        'members': members,
        'companies': companies
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


def vote(request):
    if request.method == 'POST':
        voter_id = request.POST.get('voter')
        company_id = request.POST.get('company')
        stars = request.POST.get('stars')
        
        if not all([voter_id, company_id, stars]):
            return JsonResponse({'error': 'Все поля обязательны'}, status=400)
        
        # Check if the voter has already voted for this company
        if Feedback.objects.filter(voter_id=voter_id, company_id=company_id).exists():
            return JsonResponse({'error': 'Вы уже проголосовали за эту компанию'}, status=400)
        
        try:
            feedback = Feedback.objects.create(
                voter_id=voter_id,
                company_id=company_id,
                stars=stars
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    companies = Company.objects.all()
    return render(request, 'vote.html', {
        'companies': companies
    })


def add_member(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            company_name = request.POST.get('company')
            position = request.POST.get('position')
            role = request.POST.get('role')
            
            # Check if all required fields are provided
            if not all([name, phone, company_name, position, role]):
                return JsonResponse({
                    'success': False,
                    'error': 'Все поля обязательны для заполнения'
                })
            
            # Validate phone number format
            if not phone.startswith('+'):
                return JsonResponse({
                    'success': False,
                    'error': 'Номер телефона должен начинаться с +'
                })

            # Remove all non-digit characters except +
            phone_digits = ''.join(c for c in phone if c.isdigit() or c == '+')
            
            # Check if phone number has correct length (country code + number)
            if len(phone_digits) < 12 or len(phone_digits) > 15:
                return JsonResponse({
                    'success': False,
                    'error': 'Неверный формат номера телефона'
                })
            
            # Check if phone number already exists
            if Member.objects.filter(phone=phone_digits).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Участник с таким номером телефона уже существует'
                })
            
            # Get or create company
            company, created = Company.objects.get_or_create(name=company_name.strip())
            
            # Create new member with cleaned phone number
            member = Member.objects.create(
                name=name,
                phone=phone_digits,
                company=company,
                position=position,
                role=int(role)
            )
            
            # Generate QR code
            member.create_qr_code_with_text()
            
            return JsonResponse({
                'success': True,
                'redirect_url': '/admin/api/member/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    # GET request - render the form
    companies = Company.objects.all().order_by('name')
    positions = POSITION_CHOICES.choices
    roles = ROLE_CHOISES.choices
    
    return render(request, 'add_member.html', {
        'companies': companies,
        'positions': positions,
        'roles': roles
    })


