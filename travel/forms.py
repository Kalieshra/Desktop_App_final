from django import forms
from .models import Travel, TravelType


class TravelTypeForm(forms.ModelForm):
    class Meta:
        model = TravelType
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = [
            'name', 'title', 'department', 'position', 'travel_type',
            'course_name', 'course_location', 'date_from', 'date_to',
            'deadline', 'followup', 'attachment', 'event_code', 'total_travels',
            'is_accepted', 'aps', 'publish_committee', 'visual_presentation', 'sader',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'travel_type': forms.Select(attrs={'class': 'form-select'}),
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_location': forms.TextInput(attrs={'class': 'form-control'}),
            'date_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'followup': forms.TextInput(attrs={'class': 'form-control'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'event_code': forms.TextInput(attrs={'class': 'form-control'}),
            'total_travels': forms.TextInput(attrs={'class': 'form-control'}),
            'is_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aps': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'publish_committee': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'visual_presentation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sader': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        }


class ExcelImportForm(forms.Form):
    file = forms.FileField(
        label='ملف Excel',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx,.xls'}),
    )
