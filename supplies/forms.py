from django import forms
from .models import SupplyChannel, BuyOrder, ServiceOrder, Offer, ChannelPost, ContractOperation, ATSContract, Tender


class SupplyChannelForm(forms.ModelForm):
    class Meta:
        model = SupplyChannel
        fields = ['name', 'date', 'created_by', 'is_accepted']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'created_by': forms.TextInput(attrs={'class': 'form-control'}),
            'is_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BuyOrderForm(forms.ModelForm):
    class Meta:
        model = BuyOrder
        fields = [
            'supply_channel', 'requester_name', 'job', 'location',
            'description', 'estimated_value', 'company_entity',
            # Offer checkboxes
            'offer_envap', 'offer_first', 'offer_second', 'offer_third', 'offer_divisible',
            # Committee checkboxes
            'committee_technical', 'committee_legal', 'committee_financial',
            'committee_legal_signature', 'committee_supervisor_signature',
            # Other
            'memo', 'supply_order_no', 'is_accepted', 'attachment',
        ]
        widgets = {
            'supply_channel': forms.Select(attrs={'class': 'form-select'}),
            'requester_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estimated_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'company_entity': forms.TextInput(attrs={'class': 'form-control'}),
            # Offer checkboxes
            'offer_envap': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'offer_first': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'offer_second': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'offer_third': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'offer_divisible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # Committee checkboxes
            'committee_technical': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'committee_legal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'committee_financial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'committee_legal_signature': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'committee_supervisor_signature': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # Other
            'memo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'supply_order_no': forms.TextInput(attrs={'class': 'form-control'}),
            'is_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = [
            'buy_order', 'service_order_no', 'date', 'object_description',
            'reference',
            'to_invap_reactor', 'to_invap_fuel', 'to_invap_isotopes', 'to_invap_uranium',
            'description', 'signature', 'is_accepted', 'attachment',
        ]
        widgets = {
            'buy_order': forms.HiddenInput(),
            'service_order_no': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'object_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'to_invap_reactor':  forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'to_invap_fuel':     forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'to_invap_isotopes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'to_invap_uranium':  forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'signature': forms.TextInput(attrs={'class': 'form-control'}),
            'is_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['buy_order', 'company_name', 'price', 'description', 'is_accepted', 'attachment']
        widgets = {
            'buy_order': forms.HiddenInput(),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ChannelPostForm(forms.ModelForm):
    class Meta:
        model = ChannelPost
        fields = ['supply_channel', 'name', 'date', 'description', 'attachment', 'price', 'is_accepted']
        widgets = {
            'supply_channel': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ATSContractForm(forms.ModelForm):
    class Meta:
        model = ATSContract
        fields = [
            'buy_order', 'entity', 'supply_order_no',
            'amount_dollar', 'amount_egyptian', 'statement', 'supply_duration',
            'amount_fully_disbursed', 'remaining', 'not_disbursed_current_year',
            'prev_year_2020', 'prev_year_2021', 'prev_year_2022', 'prev_year_2023',
            'prev_year_2024', 'prev_year_2025', 'prev_year_2026',
            'attachment',
        ]
        widgets = {
            'buy_order': forms.HiddenInput(),
            'entity': forms.TextInput(attrs={'class': 'form-control'}),
            'supply_order_no': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_dollar': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_egyptian': forms.NumberInput(attrs={'class': 'form-control'}),
            'statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'supply_duration': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_fully_disbursed': forms.NumberInput(attrs={
                'class': 'form-control', 'min': '0', 'max': '100',
                'step': '0.01', 'placeholder': 'e.g. 30',
            }),
            'remaining': forms.NumberInput(attrs={
                'class': 'form-control bg-light', 'readonly': 'readonly',
            }),
            'not_disbursed_current_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'prev_year_2020': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prev_year_2021': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prev_year_2022': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prev_year_2023': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prev_year_2024': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prev_year_2025': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prev_year_2026': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class TenderForm(forms.ModelForm):
    class Meta:
        model = Tender
        fields = [
            'supply_channel', 'tender_name',
            'formal_inspection_minutes', 'formal_inspection_minutes_attachment',
            'admin_formation_order', 'admin_formation_order_attachment',
            'technical_minutes', 'technical_minutes_attachment',
            'minutes_1', 'minutes_1_attachment',
            'technical_report', 'technical_report_attachment',
            'minutes_2', 'minutes_2_attachment',
            'financial_opening', 'financial_opening_attachment',
            'financial_report', 'financial_report_attachment',
            'minutes_3', 'minutes_3_attachment',
            'bid_acceptance_notification', 'bid_acceptance_notification_attachment',
            'linking', 'linking_attachment',
            'estimated_value_minutes', 'estimated_value_attachment', 'estimated_value_percentage',
            'envelope_opening_minutes', 'envelope_opening_attachment',
            'tender_type', 'tender_type_attachment',
            'attachment',
        ]
        widgets = {
            'supply_channel': forms.HiddenInput(),
            'tender_name': forms.TextInput(attrs={'class': 'form-control'}),
            'formal_inspection_minutes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'formal_inspection_minutes_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'admin_formation_order': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'admin_formation_order_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'technical_minutes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'technical_minutes_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'minutes_1': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'minutes_1_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'technical_report': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'technical_report_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'minutes_2': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'minutes_2_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'financial_opening': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'financial_opening_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'financial_report': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'financial_report_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'minutes_3': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'minutes_3_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bid_acceptance_notification': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bid_acceptance_notification_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'linking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'linking_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'estimated_value_minutes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'estimated_value_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'estimated_value_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': 'مثال: 25.50',
            }),
            'envelope_opening_minutes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'envelope_opening_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tender_type': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'tender_type_attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ContractOperationForm(forms.ModelForm):
    class Meta:
        model = ContractOperation
        fields = [
            'supply_channel', 'operation_type', 'operation_name',
            'contracting_entity', 'contract_start_date', 'assignment_method',
            'total_amount', 'amount_paid', 'notes', 'attachment',
        ]
        widgets = {
            'supply_channel': forms.HiddenInput(),
            'operation_type': forms.Select(attrs={'class': 'form-select'}),
            'operation_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contracting_entity': forms.TextInput(attrs={'class': 'form-control'}),
            'contract_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assignment_method': forms.Select(attrs={'class': 'form-select'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
