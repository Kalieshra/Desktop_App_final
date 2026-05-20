from django import forms

from .models import Budget, BudgetChapter, CHAPTER_COUNT


_NUM_ATTRS = {
    'class': 'form-control form-control-sm text-center budget-num',
    'step': '0.01',
    'min': '0',
}


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: ميزانية الربع الأول',
            }),
        }


class BudgetChapterForm(forms.ModelForm):
    class Meta:
        model = BudgetChapter
        fields = ['chapter_number', 'allocated', 'reinforcement', 'commitment', 'expenditure']
        widgets = {
            'chapter_number': forms.HiddenInput(),
            'allocated': forms.NumberInput(attrs=_NUM_ATTRS),
            'reinforcement': forms.NumberInput(attrs=_NUM_ATTRS),
            'commitment': forms.NumberInput(attrs=_NUM_ATTRS),
            'expenditure': forms.NumberInput(attrs=_NUM_ATTRS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('allocated', 'reinforcement', 'commitment', 'expenditure'):
            self.fields[name].required = False


BudgetChapterFormSet = forms.inlineformset_factory(
    Budget,
    BudgetChapter,
    form=BudgetChapterForm,
    extra=0,
    min_num=CHAPTER_COUNT,
    max_num=CHAPTER_COUNT,
    validate_min=False,
    validate_max=False,
    can_delete=False,
)
