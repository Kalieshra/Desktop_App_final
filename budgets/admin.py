from django.contrib import admin

from .models import Budget, BudgetChapter


class BudgetChapterInline(admin.TabularInline):
    model = BudgetChapter
    extra = 0
    max_num = 6


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [BudgetChapterInline]
