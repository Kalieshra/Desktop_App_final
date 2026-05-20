from django.contrib import admin
from .models import Travel


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'department', 'course_type', 'course_location', 'date_from', 'date_to']
    list_filter = ['title', 'department', 'course_type']
    search_fields = ['name', 'course_name', 'course_location', 'event_code']
    list_per_page = 25
