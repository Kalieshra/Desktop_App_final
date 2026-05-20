from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import InvestmentPlanForm, ManqoolMinhEntryFormSet
from .models import InvestmentPlan


def _recompute_manqool_totals(plan):
    """Sync the manqool_minh/_ilaih cached totals from the entries.

    Each entry's main_value is already deducted from its source field's
    modified value (done on the client). The cached totals represent the
    total amount transferred (out = in).
    """
    entries = list(plan.manqool_minh_entries.all())
    total = sum((e.main_value or Decimal('0') for e in entries), Decimal('0'))
    InvestmentPlan.objects.filter(pk=plan.pk).update(
        manqool_minh_modified=total,
        manqool_ilaih_modified=total,
    )


class InvestmentPlanListView(ListView):
    model = InvestmentPlan
    template_name = 'investments/plan_list.html'
    context_object_name = 'plans'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(name__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class _PlanFormMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'manqool_formset' not in context:
            if self.request.method == 'POST':
                context['manqool_formset'] = ManqoolMinhEntryFormSet(
                    self.request.POST, instance=self.object,
                )
            else:
                context['manqool_formset'] = ManqoolMinhEntryFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        manqool_formset = ManqoolMinhEntryFormSet(
            self.request.POST, instance=getattr(self, 'object', None),
        )
        if not manqool_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, manqool_formset=manqool_formset)
            )
        with transaction.atomic():
            self.object = form.save()
            manqool_formset.instance = self.object
            manqool_formset.save()
            _recompute_manqool_totals(self.object)
        messages.success(self.request, self._success_message)
        return HttpResponseRedirect(self.get_success_url())


class InvestmentPlanCreateView(_PlanFormMixin, CreateView):
    model = InvestmentPlan
    form_class = InvestmentPlanForm
    template_name = 'investments/plan_form.html'
    success_url = reverse_lazy('investments:plan_list')
    _success_message = 'تم إضافة خطة الاستثمار بنجاح.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'إضافة خطة استثمار'
        return context


class InvestmentPlanDetailView(DetailView):
    model = InvestmentPlan
    template_name = 'investments/plan_detail.html'
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_groups'] = self.object.get_section_groups()
        context['manqool_entries'] = self.object.manqool_minh_entries.all()
        context['manqool_total_diff'] = sum(
            ((e.main_value or Decimal('0')) for e in context['manqool_entries']),
            Decimal('0'),
        )
        return context


class InvestmentPlanUpdateView(_PlanFormMixin, UpdateView):
    model = InvestmentPlan
    form_class = InvestmentPlanForm
    template_name = 'investments/plan_form.html'
    _success_message = 'تم تعديل خطة الاستثمار بنجاح.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'تعديل: {self.object.name}'
        return context

    def get_success_url(self):
        return reverse('investments:plan_detail', kwargs={'pk': self.object.pk})


class InvestmentPlanDeleteView(DeleteView):
    model = InvestmentPlan
    template_name = 'investments/confirm_delete.html'
    success_url = reverse_lazy('investments:plan_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف خطة الاستثمار بنجاح.')
        return super().form_valid(form)
