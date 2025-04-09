from django.contrib import admin
from .models import Member, Company, Feedback
from django.db.models import Sum


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'position', 'phone', 'role')
    list_filter = ('role', 'company')
    search_fields = ('name', 'company__name', 'phone')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_total_points')
    search_fields = ('name',)

    def get_total_points(self, obj):
        """Safely calculate total points for each company."""
        total = Feedback.objects.filter(company=obj).aggregate(total_points=Sum('stars'))['total_points']
        return total or 0
    get_total_points.short_description = 'Total Points'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_id', 'company', 'stars', 'created_at')
    list_filter = ('member_id', 'company')
    search_fields = ('member_id__name', 'company__name')

