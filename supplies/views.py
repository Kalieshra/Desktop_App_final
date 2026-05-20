from itertools import chain
from operator import attrgetter

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import (
    SupplyChannelForm, BuyOrderForm, ServiceOrderForm, OfferForm, ChannelPostForm,
    ContractOperationForm, ATSContractForm, TenderForm,
)
from .models import SupplyChannel, BuyOrder, ServiceOrder, Offer, ChannelPost, ContractOperation, ATSContract, Tender


# ── SupplyChannel Views ────────────────────────────────────────

class SupplyChannelListView(ListView):
    model = SupplyChannel
    template_name = 'supplies/channel_list.html'
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


class SupplyChannelDetailView(DetailView):
    model = SupplyChannel
    template_name = 'supplies/channel_detail.html'
    context_object_name = 'channel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Existing records
        buy_orders = list(self.object.buy_orders.all())
        posts = list(self.object.posts.all())

        # Collect offers and service orders from all buy orders
        offers = []
        service_orders = []

        for buy_order in buy_orders:
            offers.extend(list(buy_order.offers.all()))
            service_orders.extend(list(buy_order.service_orders.all()))

        # Set record types
        for item in buy_orders:
            item.record_type = 'buy_order'
        for item in posts:
            item.record_type = 'post'
        for item in offers:
            item.record_type = 'offer'
        for item in service_orders:
            item.record_type = 'service_order'

        # Combine all records and sort chronologically
        all_records = sorted(
            chain(buy_orders, posts, offers, service_orders),
            key=attrgetter('created_at'),
        )

        context['records'] = all_records
        context['contract_operations'] = self.object.contract_operations.all()
        context['tenders'] = self.object.tenders.all()
        return context


class SupplyChannelCreateView(CreateView):
    model = SupplyChannel
    form_class = SupplyChannelForm
    template_name = 'supplies/channel_form.html'
    success_url = reverse_lazy('supplies:channel_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة القناة بنجاح.')
        return super().form_valid(form)


class SupplyChannelUpdateView(UpdateView):
    model = SupplyChannel
    form_class = SupplyChannelForm
    template_name = 'supplies/channel_form.html'
    success_url = reverse_lazy('supplies:channel_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل القناة بنجاح.')
        return super().form_valid(form)


class SupplyChannelDeleteView(DeleteView):
    model = SupplyChannel
    template_name = 'supplies/confirm_delete.html'
    success_url = reverse_lazy('supplies:channel_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف القناة بنجاح.')
        return super().form_valid(form)


# ── BuyOrder Views ─────────────────────────────────────────────

class BuyOrderCreateView(CreateView):
    model = BuyOrder
    form_class = BuyOrderForm
    template_name = 'supplies/buy_order_form.html'

    def get_initial(self):
        initial = super().get_initial()
        channel_pk = self.request.GET.get('channel')
        if channel_pk:
            initial['supply_channel'] = channel_pk
        return initial

    def get_success_url(self):
        return reverse('supplies:channel_detail', kwargs={'pk': self.object.supply_channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة طلب الشراء بنجاح.')
        return super().form_valid(form)


class BuyOrderDetailView(DetailView):
    model = BuyOrder
    template_name = 'supplies/buy_order_detail.html'
    context_object_name = 'buy_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_order = self.object.service_orders.first()
        context['service_order'] = service_order
        context['offers'] = self.object.offers.all()
        context['service_order_form'] = ServiceOrderForm(
            initial={'buy_order': self.object.pk}
        )
        context['offer_form'] = OfferForm(
            initial={'buy_order': self.object.pk}
        )
        context['ats_contracts'] = self.object.ats_contracts.all()
        context['ats_contract_form'] = ATSContractForm(
            initial={'buy_order': self.object.pk}
        )
        return context


class BuyOrderUpdateView(UpdateView):
    model = BuyOrder
    form_class = BuyOrderForm
    template_name = 'supplies/buy_order_form.html'

    def get_success_url(self):
        return reverse('supplies:buy_order_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل طلب الشراء بنجاح.')
        return super().form_valid(form)


class BuyOrderDeleteView(DeleteView):
    model = BuyOrder
    template_name = 'supplies/confirm_delete.html'

    def get_success_url(self):
        return reverse('supplies:channel_detail', kwargs={'pk': self.object.supply_channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف طلب الشراء بنجاح.')
        return super().form_valid(form)


# ── ServiceOrder Views ─────────────────────────────────────────

class ServiceOrderCreateView(CreateView):
    model = ServiceOrder
    form_class = ServiceOrderForm
    template_name = 'supplies/service_order_form.html'

    def get_initial(self):
        initial = super().get_initial()
        buy_order_pk = self.request.GET.get('buy_order')
        if buy_order_pk:
            initial['buy_order'] = buy_order_pk
        return initial

    def get_success_url(self):
        return reverse('supplies:buy_order_detail', kwargs={'pk': self.object.buy_order_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة أمر الخدمة بنجاح.')
        return super().form_valid(form)


class ServiceOrderUpdateView(UpdateView):
    model = ServiceOrder
    form_class = ServiceOrderForm
    template_name = 'supplies/service_order_form.html'

    def get_success_url(self):
        return reverse('supplies:buy_order_detail', kwargs={'pk': self.object.buy_order_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل أمر الخدمة بنجاح.')
        return super().form_valid(form)


class ServiceOrderDeleteView(DeleteView):
    model = ServiceOrder
    template_name = 'supplies/confirm_delete.html'

    def get_success_url(self):
        return reverse('supplies:buy_order_detail', kwargs={'pk': self.object.buy_order_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف أمر الخدمة بنجاح.')
        return super().form_valid(form)


# ── Offer Views ────────────────────────────────────────────────

class OfferCreateView(CreateView):
    model = Offer
    form_class = OfferForm
    template_name = 'supplies/offer_form.html'

    def get_initial(self):
        initial = super().get_initial()
        buy_order_pk = self.request.GET.get('buy_order')
        if buy_order_pk:
            initial['buy_order'] = buy_order_pk
        return initial

    def get_success_url(self):
        return reverse('supplies:buy_order_detail', kwargs={'pk': self.object.buy_order_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة العرض بنجاح.')
        return super().form_valid(form)


class OfferUpdateView(UpdateView):
    model = Offer
    form_class = OfferForm
    template_name = 'supplies/offer_form.html'

    def get_success_url(self):
        return reverse('supplies:buy_order_detail', kwargs={'pk': self.object.buy_order_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل العرض بنجاح.')
        return super().form_valid(form)


class OfferDeleteView(DeleteView):
    model = Offer
    template_name = 'supplies/confirm_delete.html'

    def get_success_url(self):
        return reverse('supplies:buy_order_detail', kwargs={'pk': self.object.buy_order_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف العرض بنجاح.')
        return super().form_valid(form)


class OfferSelectView(View):
    def post(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        Offer.objects.filter(buy_order=offer.buy_order).update(is_selected=False)
        offer.is_selected = True
        offer.save()
        messages.success(request, 'تم اختيار العرض بنجاح.')
        return redirect('supplies:buy_order_detail', pk=offer.buy_order_id)


# ── ChannelPost Views ──────────────────────────────────────────

class ChannelPostCreateView(CreateView):
    model = ChannelPost
    form_class = ChannelPostForm
    template_name = 'supplies/channel_post_form.html'

    def get_initial(self):
        initial = super().get_initial()
        channel_pk = self.request.GET.get('channel')
        if channel_pk:
            initial['supply_channel'] = channel_pk
        return initial

    def get_success_url(self):
        return reverse('supplies:channel_detail', kwargs={'pk': self.object.supply_channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة المنشور بنجاح.')
        return super().form_valid(form)


class ChannelPostUpdateView(UpdateView):
    model = ChannelPost
    form_class = ChannelPostForm
    template_name = 'supplies/channel_post_form.html'

    def get_success_url(self):
        return reverse('supplies:channel_detail', kwargs={'pk': self.object.supply_channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل المنشور بنجاح.')
        return super().form_valid(form)


class ChannelPostDeleteView(DeleteView):
    model = ChannelPost
    template_name = 'supplies/confirm_delete.html'

    def get_success_url(self):
        return reverse('supplies:channel_detail', kwargs={'pk': self.object.supply_channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف المنشور بنجاح.')
        return super().form_valid(form)


# ── Toggle Accept Views ────────────────────────────────────────

class SupplyChannelToggleAcceptView(View):
    def post(self, request, pk):
        obj = get_object_or_404(SupplyChannel, pk=pk)
        obj.is_accepted = not obj.is_accepted
        obj.save()
        messages.success(request, 'تم تحديث حالة القناة بنجاح.')
        return redirect('supplies:channel_list')


class BuyOrderToggleAcceptView(View):
    def post(self, request, pk):
        obj = get_object_or_404(BuyOrder, pk=pk)
        obj.is_accepted = not obj.is_accepted
        obj.save()
        messages.success(request, 'تم تحديث حالة طلب الشراء بنجاح.')
        return redirect('supplies:channel_detail', pk=obj.supply_channel_id)


class ServiceOrderToggleAcceptView(View):
    def post(self, request, pk):
        obj = get_object_or_404(ServiceOrder, pk=pk)
        obj.is_accepted = not obj.is_accepted
        obj.save()
        messages.success(request, 'تم تحديث حالة أمر الخدمة بنجاح.')
        return redirect('supplies:buy_order_detail', pk=obj.buy_order_id)


class OfferToggleAcceptView(View):
    def post(self, request, pk):
        obj = get_object_or_404(Offer, pk=pk)
        obj.is_accepted = not obj.is_accepted
        obj.save()
        messages.success(request, 'تم تحديث حالة العرض بنجاح.')
        return redirect('supplies:buy_order_detail', pk=obj.buy_order_id)


class ChannelPostToggleAcceptView(View):
    def post(self, request, pk):
        obj = get_object_or_404(ChannelPost, pk=pk)
        obj.is_accepted = not obj.is_accepted
        obj.save()
        messages.success(request, 'تم تحديث حالة المنشور بنجاح.')
        return redirect('supplies:channel_detail', pk=obj.supply_channel_id)


# ── Tender Views ──────────────────────────────────────────────────

class TenderListView(ListView):
    model = Tender
    template_name = 'supplies/tender_list.html'
    context_object_name = 'tenders'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        channel_pk = self.request.GET.get('channel', '').strip()
        q = self.request.GET.get('q', '').strip()
        if channel_pk:
            qs = qs.filter(supply_channel_id=channel_pk)
        if q:
            qs = qs.filter(tender_name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['channels'] = SupplyChannel.objects.all()
        context['selected_channel'] = self.request.GET.get('channel', '')
        return context


class TenderCreateView(CreateView):
    model = Tender
    form_class = TenderForm
    template_name = 'supplies/tender_form.html'

    def get_initial(self):
        initial = super().get_initial()
        channel_pk = self.request.GET.get('channel')
        if channel_pk:
            initial['supply_channel'] = channel_pk
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel_pk = self.request.GET.get('channel') or self.request.POST.get('supply_channel')
        if channel_pk:
            context['channel'] = get_object_or_404(SupplyChannel, pk=channel_pk)
        return context

    def get_success_url(self):
        return reverse('supplies:channel_detail', kwargs={'pk': self.object.supply_channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة المناقصة بنجاح.')
        return super().form_valid(form)


class TenderUpdateView(UpdateView):
    model = Tender
    form_class = TenderForm
    template_name = 'supplies/tender_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['channel'] = self.object.supply_channel
        return context

    def get_success_url(self):
        return reverse('supplies:channel_detail', kwargs={'pk': self.object.supply_channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل المناقصة بنجاح.')
        return super().form_valid(form)


class TenderDeleteView(DeleteView):
    model = Tender
    template_name = 'supplies/confirm_delete.html'

    def get_success_url(self):
        return reverse('supplies:channel_detail', kwargs={'pk': self.object.supply_channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف المناقصة بنجاح.')
        return super().form_valid(form)


# ── ATSContract Views ─────────────────────────────────────────────

class ATSContractCreateView(CreateView):
    model = ATSContract
    form_class = ATSContractForm
    template_name = 'supplies/buy_order_detail.html'

    def get_success_url(self):
        return reverse('supplies:buy_order_detail', kwargs={'pk': self.object.buy_order_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة عقد ATS بنجاح.')
        return super().form_valid(form)

    def form_invalid(self, form):
        buy_order_pk = form.data.get('buy_order')
        messages.error(self.request, 'حدث خطأ أثناء حفظ عقد ATS.')
        return redirect('supplies:buy_order_detail', pk=buy_order_pk)


class ATSContractUpdateView(UpdateView):
    model = ATSContract
    form_class = ATSContractForm
    template_name = 'supplies/ats_contract_form.html'

    def get_success_url(self):
        return reverse('supplies:buy_order_detail', kwargs={'pk': self.object.buy_order_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل عقد ATS بنجاح.')
        return super().form_valid(form)


class ATSContractDeleteView(DeleteView):
    model = ATSContract
    template_name = 'supplies/confirm_delete.html'

    def get_success_url(self):
        return reverse('supplies:buy_order_detail', kwargs={'pk': self.object.buy_order_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف عقد ATS بنجاح.')
        return super().form_valid(form)


# ── ContractOperation Views ────────────────────────────────────

class ContractOperationCreateView(CreateView):
    model = ContractOperation
    form_class = ContractOperationForm
    template_name = 'supplies/contract_operation_form.html'

    def get_initial(self):
        initial = super().get_initial()
        channel_pk = self.request.GET.get('channel')
        if channel_pk:
            initial['supply_channel'] = channel_pk
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel_pk = self.request.GET.get('channel') or self.request.POST.get('supply_channel')
        if channel_pk:
            context['channel'] = get_object_or_404(SupplyChannel, pk=channel_pk)
        return context

    def get_success_url(self):
        return reverse('supplies:channel_detail', kwargs={'pk': self.object.supply_channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة العملية بنجاح.')
        return super().form_valid(form)


class ContractOperationUpdateView(UpdateView):
    model = ContractOperation
    form_class = ContractOperationForm
    template_name = 'supplies/contract_operation_form.html'

    def get_success_url(self):
        return reverse('supplies:channel_detail', kwargs={'pk': self.object.supply_channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم تعديل العملية بنجاح.')
        return super().form_valid(form)


class ContractOperationDeleteView(DeleteView):
    model = ContractOperation
    template_name = 'supplies/confirm_delete.html'

    def get_success_url(self):
        return reverse('supplies:channel_detail', kwargs={'pk': self.object.supply_channel_id})

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف العملية بنجاح.')
        return super().form_valid(form)
