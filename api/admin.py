from django.contrib import admin
from .models import *


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'id','company', 'phone', 'position', 'expo', 'role', 'registration_time')
    search_fields = ('name', 'email', 'phone', 'company') 
    list_filter = ('expo', 'role') 



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_id', 'feedback_body','audio_feedback')


#!GIT PUSH