from django import forms
from .models import InvestmentPlan, ManqoolMinhEntry

_num_widget = lambda: forms.NumberInput(attrs={
    'class': 'form-control form-control-sm text-center',
    'step': '0.01',
    'min': '0',
})

_NUMERIC_FIELDS = [
    'lands', 'residential_buildings', 'non_residential_buildings',
    'constructions',
    'machinery_local', 'machinery_foreign', 'machinery_self_financed',
    'transport_means', 'furniture_equipment', 'livestock', 'transport_subtotal',
    'setup_preparations', 'transport_travel_expenses', 'research_studies', 'setup_subtotal',
    'total_fixed_investment', 'advance_payments', 'grand_total',
    'manqool_minh', 'manqool_ilaih', 'nisbat_munaffaz', 'mutayyiqas',
]


_EXCLUDE_FIELDS = [f'{key}_project' for key in _NUMERIC_FIELDS]


class InvestmentPlanForm(forms.ModelForm):
    class Meta:
        model = InvestmentPlan
        exclude = _EXCLUDE_FIELDS
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in _NUMERIC_FIELDS:
            for suffix in ('original', 'modified'):
                field_name = f'{key}_{suffix}'
                if field_name in self.fields:
                    self.fields[field_name].widget = _num_widget()
                    self.fields[field_name].required = False


class ManqoolMinhEntryForm(forms.ModelForm):
    class Meta:
        model = ManqoolMinhEntry
        fields = ['source_field', 'main_value']
        widgets = {
            'source_field': forms.Select(attrs={
                'class': 'form-select form-select-sm manqool-source',
            }),
            'main_value': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm text-center manqool-main',
                'step': '0.01',
                'min': '0',
            }),
        }


ManqoolMinhEntryFormSet = forms.inlineformset_factory(
    InvestmentPlan,
    ManqoolMinhEntry,
    form=ManqoolMinhEntryForm,
    extra=0,
    can_delete=True,
)
