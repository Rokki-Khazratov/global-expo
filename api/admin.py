from django.contrib import admin
from .models import *

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'position', 'registration_date')
    list_filter = ('company', 'registration_date')
    search_fields = ('name', 'email', 'company')
    ordering = ('-registration_date',)

    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'company', 'position', 'phone')
        }),
        ('Дополнительная информация', {
            'fields': ('registration_date',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('registration_date',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_id', 'feedback_body','audio_feedback')
