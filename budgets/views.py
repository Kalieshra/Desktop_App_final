from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import BudgetChapterFormSet, BudgetForm
from .models import Budget, BudgetChapter, CHAPTER_COUNT


def _initial_chapters():
    return [{'chapter_number': i} for i in range(1, CHAPTER_COUNT + 1)]


class BudgetListView(ListView):
    model = Budget
    template_name = 'budgets/budget_list.html'
    context_object_name = 'budgets'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('chapters')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(name__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class _BudgetFormMixin:
    def get_formset(self):
        if self.request.method == 'POST':
            return BudgetChapterFormSet(self.request.POST, instance=self.object)
        if self.object is None:
            return BudgetChapterFormSet(
                instance=Budget(),
                initial=_initial_chapters(),
            )
        return BudgetChapterFormSet(instance=self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('chapter_formset', self.get_formset())
        return context

    def form_valid(self, form):
        formset = BudgetChapterFormSet(
            self.request.POST,
            instance=getattr(self, 'object', None) or Budget(),
        )
        if not formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, chapter_formset=formset)
            )
        with transaction.atomic():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            self.object.ensure_chapters()
        messages.success(self.request, self._success_message)
        return HttpResponseRedirect(self.get_success_url())


class BudgetCreateView(_BudgetFormMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budgets:budget_list')
    _success_message = 'تم إضافة الميزانية بنجاح.'
    object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'إضافة ميزانية جديدة'
        return context


class BudgetUpdateView(_BudgetFormMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    _success_message = 'تم تعديل الميزانية بنجاح.'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.ensure_chapters()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'تعديل: {self.object.name}'
        return context

    def get_success_url(self):
        return reverse('budgets:budget_detail', kwargs={'pk': self.object.pk})


class BudgetDetailView(DetailView):
    model = Budget
    template_name = 'budgets/budget_detail.html'
    context_object_name = 'budget'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.ensure_chapters()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapters = list(self.object.chapters.all())
        context['chapters'] = chapters
        context['totals'] = {
            'allocated': self.object.total_allocated,
            'reinforcement': self.object.total_reinforcement,
            'commitment': self.object.total_commitment,
            'expenditure': self.object.total_expenditure,
            'remaining': self.object.total_remaining,
        }
        return context


class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = 'budgets/confirm_delete.html'
    success_url = reverse_lazy('budgets:budget_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف الميزانية بنجاح.')
        return super().form_valid(form)
