from django.contrib import admin
from .models import InvestmentPlan


@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'grand_total_original', 'grand_total_modified', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
