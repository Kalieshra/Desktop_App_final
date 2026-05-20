from django import forms
from .models import Channel, PlaceLicense, PersonalLicense, Inspection


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'date', 'created_by', 'is_accepted']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'created_by': forms.TextInput(attrs={'class': 'form-control'}),
            'is_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PlaceLicenseForm(forms.ModelForm):
    class Meta:
        model = PlaceLicense
        fields = ['channel', 'license_duration', 'date_from', 'date_to', 'is_paid', 'is_accepted', 'attachment']
        widgets = {
            'channel': forms.Select(attrs={'class': 'form-select'}),
            'license_duration': forms.TextInput(attrs={'class': 'form-control'}),
            'date_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PersonalLicenseForm(forms.ModelForm):
    class Meta:
        model = PersonalLicense
        fields = [
            'channel', 'applicant_name', 'category', 'job', 'phone',
            'license_type', 'date_from', 'date_to', 'license_duration',
            'is_paid', 'is_accepted', 'attachment',
        ]
        widgets = {
            'channel': forms.Select(attrs={'class': 'form-select'}),
            'applicant_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'job': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'license_type': forms.Select(attrs={'class': 'form-select'}),
            'date_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'license_duration': forms.Select(attrs={'class': 'form-select'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['channel', 'inspector_name', 'job', 'authority', 'visit_date', 'result', 'is_accepted', 'attachment']
        widgets = {
            'channel': forms.Select(attrs={'class': 'form-select'}),
            'inspector_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job': forms.TextInput(attrs={'class': 'form-control'}),
            'authority': forms.Select(attrs={'class': 'form-select'}),
            'visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'result': forms.Select(attrs={'class': 'form-select'}),
            'is_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
