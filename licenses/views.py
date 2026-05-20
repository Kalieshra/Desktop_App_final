from itertools import chain
from operator import attrgetter

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ChannelForm, PlaceLicenseForm, PersonalLicenseForm, InspectionForm
from .models import Channel, PlaceLicense, PersonalLicense, Inspection


# ── Channel Views ──────────────────────────────────────────────

class ChannelListView(ListView):
    model = Channel
    template_name = 'licenses/channel_list.html'
    context_object_name = 'channels'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(created_by__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class ChannelDetailView(DetailView):
    model = Channel
    template_name = 'licenses/channel_detail.html'
    context_object_name = 'channel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place = list(self.object.place_licenses.all())
        personal = list(self.object.personal_licenses.all())
        inspections = list(self.object.inspections.all())

        for item in place:
            item.record_type = 'place_license'
        for item in personal:
            item.record_type = 'personal_license'
        for item in inspections:
            item.record_type = 'inspection'

        all_records = sorted(
            chain(place, personal, inspections),
            key=attrgetter('created_at'),
        )
        context['records'] = all_records
        return context


class ChannelCreateView(CreateView):
    model = Channel
    form_class = ChannelForm
    template_name = 'licenses/channel_form.html'
    success_url = reverse_lazy('licenses:channel_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة القناة بنجاح.')
        return super().form_valid(form)


class ChannelUpdateView(UpdateView):
    model = Channel
    form_class = ChannelForm
    template_name = 'licenses/channel_form.html'
    success_url = reverse_lazy('licenses:channel_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل القناة بنجاح.')
        return super().form_valid(form)


class ChannelDeleteView(DeleteView):
    model = Channel
    template_name = 'licenses/confirm_delete.html'
    success_url = reverse_lazy('licenses:channel_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف القناة بنجاح.')
        return super().form_valid(form)


# ── PlaceLicense Views ─────────────────────────────────────────

class PlaceLicenseCreateView(CreateView):
    model = PlaceLicense
    form_class = PlaceLicenseForm
    template_name = 'licenses/place_license_form.html'

    def get_initial(self):
        initial = super().get_initial()
        channel_pk = self.request.GET.get('channel')
        if channel_pk:
            initial['channel'] = channel_pk
        return initial

    def get_success_url(self):
        return reverse('licenses:channel_detail', kwargs={'pk': self.object.channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة الترخيص المكاني بنجاح.')
        return super().form_valid(form)


class PlaceLicenseUpdateView(UpdateView):
    model = PlaceLicense
    form_class = PlaceLicenseForm
    template_name = 'licenses/place_license_form.html'

    def get_success_url(self):
        return reverse('licenses:channel_detail', kwargs={'pk': self.object.channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل الترخيص المكاني بنجاح.')
        return super().form_valid(form)


class PlaceLicenseDeleteView(DeleteView):
    model = PlaceLicense
    template_name = 'licenses/confirm_delete.html'

    def get_success_url(self):
        return reverse('licenses:channel_detail', kwargs={'pk': self.object.channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف الترخيص المكاني بنجاح.')
        return super().form_valid(form)


# ── PersonalLicense Views ──────────────────────────────────────

class PersonalLicenseCreateView(CreateView):
    model = PersonalLicense
    form_class = PersonalLicenseForm
    template_name = 'licenses/personal_license_form.html'

    def get_initial(self):
        initial = super().get_initial()
        channel_pk = self.request.GET.get('channel')
        if channel_pk:
            initial['channel'] = channel_pk
        return initial

    def get_success_url(self):
        return reverse('licenses:channel_detail', kwargs={'pk': self.object.channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة الترخيص الشخصي بنجاح.')
        return super().form_valid(form)


class PersonalLicenseUpdateView(UpdateView):
    model = PersonalLicense
    form_class = PersonalLicenseForm
    template_name = 'licenses/personal_license_form.html'

    def get_success_url(self):
        return reverse('licenses:channel_detail', kwargs={'pk': self.object.channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل الترخيص الشخصي بنجاح.')
        return super().form_valid(form)


class PersonalLicenseDeleteView(DeleteView):
    model = PersonalLicense
    template_name = 'licenses/confirm_delete.html'

    def get_success_url(self):
        return reverse('licenses:channel_detail', kwargs={'pk': self.object.channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف الترخيص الشخصي بنجاح.')
        return super().form_valid(form)


# ── Inspection Views ───────────────────────────────────────────

class InspectionCreateView(CreateView):
    model = Inspection
    form_class = InspectionForm
    template_name = 'licenses/inspection_form.html'

    def get_initial(self):
        initial = super().get_initial()
        channel_pk = self.request.GET.get('channel')
        if channel_pk:
            initial['channel'] = channel_pk
        return initial

    def get_success_url(self):
        return reverse('licenses:channel_detail', kwargs={'pk': self.object.channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة التفتيش بنجاح.')
        return super().form_valid(form)


class InspectionUpdateView(UpdateView):
    model = Inspection
    form_class = InspectionForm
    template_name = 'licenses/inspection_form.html'

    def get_success_url(self):
        return reverse('licenses:channel_detail', kwargs={'pk': self.object.channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل التفتيش بنجاح.')
        return super().form_valid(form)


class InspectionDeleteView(DeleteView):
    model = Inspection
    template_name = 'licenses/confirm_delete.html'

    def get_success_url(self):
        return reverse('licenses:channel_detail', kwargs={'pk': self.object.channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف التفتيش بنجاح.')
        return super().form_valid(form)


# ── Toggle Accept Views ────────────────────────────────────────

class ChannelToggleAcceptView(View):
    def post(self, request, pk):
        obj = get_object_or_404(Channel, pk=pk)
        obj.is_accepted = not obj.is_accepted
        obj.save()
        messages.success(request, 'تم تحديث حالة القناة بنجاح.')
        return redirect('licenses:channel_list')


class PlaceLicenseToggleAcceptView(View):
    def post(self, request, pk):
        obj = get_object_or_404(PlaceLicense, pk=pk)
        obj.is_accepted = not obj.is_accepted
        obj.save()
        messages.success(request, 'تم تحديث حالة الترخيص المكاني بنجاح.')
        return redirect('licenses:channel_detail', pk=obj.channel_id)


class PersonalLicenseToggleAcceptView(View):
    def post(self, request, pk):
        obj = get_object_or_404(PersonalLicense, pk=pk)
        obj.is_accepted = not obj.is_accepted
        obj.save()
        messages.success(request, 'تم تحديث حالة الترخيص الشخصي بنجاح.')
        return redirect('licenses:channel_detail', pk=obj.channel_id)


class InspectionToggleAcceptView(View):
    def post(self, request, pk):
        obj = get_object_or_404(Inspection, pk=pk)
        obj.is_accepted = not obj.is_accepted
        obj.save()
        messages.success(request, 'تم تحديث حالة التفتيش بنجاح.')
        return redirect('licenses:channel_detail', pk=obj.channel_id)
