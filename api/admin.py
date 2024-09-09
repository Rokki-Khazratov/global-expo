from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company', 'position', 'registration_date')
    list_filter = ('company', 'registration_date')
    search_fields = ('first_name', 'last_name', 'email', 'company')
    ordering = ('-registration_date',)

    fieldsets = (
        (None, {
            'fields': ('first_name', 'email', 'company', 'position', 'phone')
        }),
        ('Дополнительная информация', {
            'fields': ('registration_date',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('registration_date',)
