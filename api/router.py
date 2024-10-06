from django.urls import path
from .views import *

urlpatterns = [
    path('members/', MemberListCreateView.as_view(), name='member-list-create'),
    path('members/<int:pk>/', MemberRetrieveUpdateDestroyView.as_view(), name='member-retrieve-update-destroy'),

    path('feedback/', FeedbackListCreateView.as_view(), name='feedback-list-create'),
    path('feedback/<int:pk>/', FeedbackRetrieveUpdateDestroyView.as_view(), name='feedback-retrieve-update-destroy'),

    path('check-member/', CheckMemberAPIView.as_view(), name='check-member'),
    path('check-qr-code/', CheckQRCodeView.as_view(), name='check-qr-code'),


]
