from django.contrib import admin
from .models import SupplyChannel, BuyOrder, ServiceOrder, Offer, ChannelPost, ATSContract, Tender


@admin.register(SupplyChannel)
class SupplyChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'created_by', 'created_at']
    search_fields = ['name', 'created_by']
    list_per_page = 25


@admin.register(BuyOrder)
class BuyOrderAdmin(admin.ModelAdmin):
    list_display = ['requester_name', 'supply_channel', 'job', 'location', 'estimated_value', 'created_at']
    list_filter = ['supply_channel']
    search_fields = ['requester_name', 'job', 'location', 'description']
    list_per_page = 25


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ['service_order_no', 'buy_order', 'date', 'created_at']
    list_filter = ['date']
    search_fields = ['service_order_no', 'object_description', 'reference']
    list_per_page = 25


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'buy_order', 'price', 'is_selected', 'created_at']
    list_filter = ['is_selected', 'buy_order']
    search_fields = ['company_name', 'description']
    list_per_page = 25


@admin.register(ChannelPost)
class ChannelPostAdmin(admin.ModelAdmin):
    list_display = ['name', 'supply_channel', 'date', 'price', 'created_at']
    list_filter = ['supply_channel']
    search_fields = ['name', 'description']
    list_per_page = 25


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ['tender_name', 'supply_channel', 'created_at']
    list_filter = ['supply_channel']
    search_fields = ['tender_name']
    list_per_page = 25


@admin.register(ATSContract)
class ATSContractAdmin(admin.ModelAdmin):
    list_display = ['entity', 'buy_order', 'supply_order_no', 'amount_dollar', 'amount_egyptian', 'created_at']
    list_filter = ['buy_order']
    search_fields = ['entity', 'supply_order_no', 'statement']
    list_per_page = 25
