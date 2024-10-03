from django.urls import path
from .views import *

urlpatterns = [
    path('members/', MemberListCreateView.as_view(), name='member-list-create'),
    path('members/<int:pk>/', MemberRetrieveUpdateDestroyView.as_view(), name='member-retrieve-update-destroy'),
    path('check-member/', CheckMemberAPIView.as_view(), name='check-member'),
    path('check-qr-code/', CheckQRCodeView.as_view(), name='check-qr-code'),


]
