from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



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


@user_passes_test(lambda u: u.is_superuser)
def members_list_view(request):
    # Get all members
    members = Member.objects.all().order_by('name')
    
    # Get filter parameters
    company_filter = request.GET.get('company')
    position_filter = request.GET.get('position')
    role_filter = request.GET.get('role')
    search_query = request.GET.get('search')
    
    # Apply filters
    if company_filter:
        members = members.filter(company__id=company_filter)
    if position_filter:
        members = members.filter(position__id=position_filter)
    if role_filter:
        members = members.filter(role=role_filter)
    if search_query:
        members = members.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(company__name__icontains=search_query)
        )
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(members, 50)
    
    try:
        members_page = paginator.page(page)
    except PageNotAnInteger:
        members_page = paginator.page(1)
    except EmptyPage:
        members_page = paginator.page(paginator.num_pages)
    
    # Get unique companies and positions for filters
    companies = Company.objects.all().order_by('name')
    positions = Position.objects.all().order_by('name')
    
    return render(request, 'members_list.html', {
        'members': members_page,
        'companies': companies,
        'positions': positions,
        'roles': ROLE_CHOISES.choices,
        'current_filters': {
            'company': company_filter,
            'position': position_filter,
            'role': role_filter,
            'search': search_query
        }
    })

def add_member(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            company_name = request.POST.get('company')
            position_id = request.POST.get('position')
            role = request.POST.get('role')
            
            # Check if all required fields are provided
            if not all([name, phone, company_name, position_id, role]):
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
            
            # Get position
            try:
                position = Position.objects.get(id=position_id)
            except Position.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Выбранная должность не существует'
                })
            
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
                'redirect_url': f'/qr-code/{member.id}/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    # GET request - render the form
    companies = Company.objects.all().order_by('name')
    positions = Position.objects.all().order_by('name')
    roles = ROLE_CHOISES.choices
    
    return render(request, 'add_member.html', {
        'companies': companies,
        'positions': positions,
        'roles': roles
    })

def view_qr_code(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    return render(request, 'view_qr.html', {
        'member': member,
        'qr_code_url': member.qr_code.url if member.qr_code else None
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('company_list')  # Redirect to company list after successful login
        else:
            return render(request, 'login.html', {
                'error_message': 'Неверное имя пользователя или пароль'
            })
    
    return render(request, 'login.html')


