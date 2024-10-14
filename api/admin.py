from django.contrib import admin
from .models import *


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'id','company', 'phone', 'position', 'expo', 'role', 'registration_time')
    search_fields = ('name','id','company') 
    list_filter = ('expo', 'role') 







@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_id','bank','stars','created_at')
    search_fields = ('id','member_id','company')
    list_filter = ('member_id','bank') 



@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_total_points')

    def get_total_points(self, obj):
        """Safely calculate total points for each bank."""
        total = Feedback.objects.filter(bank=obj).aggregate(total_points=Sum('stars'))['total_points']
        return total or 0  # Return 0 if no feedback is available

    get_total_points.short_description = 'Total Points'

