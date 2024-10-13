from django.contrib import admin
from .models import *


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'id','company', 'phone', 'position', 'expo', 'role', 'registration_time')
    search_fields = ('name','id','company') 
    list_filter = ('expo', 'role') 




@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name','id') 



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_id', 'feedback_body','bank','stars')