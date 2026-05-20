from django.contrib import admin
from .models import Channel, PlaceLicense, PersonalLicense, Inspection


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'created_by', 'created_at']
    search_fields = ['name', 'created_by']
    list_per_page = 25


@admin.register(PlaceLicense)
class PlaceLicenseAdmin(admin.ModelAdmin):
    list_display = ['channel', 'license_duration', 'date_from', 'date_to', 'is_paid']
    list_filter = ['is_paid', 'channel']
    list_per_page = 25


@admin.register(PersonalLicense)
class PersonalLicenseAdmin(admin.ModelAdmin):
    list_display = ['applicant_name', 'channel', 'category', 'license_type', 'date_from', 'date_to', 'is_paid']
    list_filter = ['category', 'license_type', 'is_paid', 'channel']
    search_fields = ['applicant_name', 'job', 'phone']
    list_per_page = 25


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ['inspector_name', 'channel', 'authority', 'visit_date', 'result']
    list_filter = ['authority', 'result', 'channel']
    search_fields = ['inspector_name', 'job']
    list_per_page = 25
