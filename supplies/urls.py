from django.urls import path
from . import views

app_name = 'supplies'

urlpatterns = [
    # SupplyChannel
    path('', views.SupplyChannelListView.as_view(), name='channel_list'),
    path('channel/add/', views.SupplyChannelCreateView.as_view(), name='channel_create'),
    path('channel/<int:pk>/', views.SupplyChannelDetailView.as_view(), name='channel_detail'),
    path('channel/<int:pk>/edit/', views.SupplyChannelUpdateView.as_view(), name='channel_update'),
    path('channel/<int:pk>/delete/', views.SupplyChannelDeleteView.as_view(), name='channel_delete'),
    path('channel/<int:pk>/toggle-accept/', views.SupplyChannelToggleAcceptView.as_view(), name='channel_toggle_accept'),

    # BuyOrder
    path('buy-order/add/', views.BuyOrderCreateView.as_view(), name='buy_order_create'),
    path('buy-order/<int:pk>/', views.BuyOrderDetailView.as_view(), name='buy_order_detail'),
    path('buy-order/<int:pk>/edit/', views.BuyOrderUpdateView.as_view(), name='buy_order_update'),
    path('buy-order/<int:pk>/delete/', views.BuyOrderDeleteView.as_view(), name='buy_order_delete'),
    path('buy-order/<int:pk>/toggle-accept/', views.BuyOrderToggleAcceptView.as_view(), name='buy_order_toggle_accept'),

    # ServiceOrder
    path('service-order/add/', views.ServiceOrderCreateView.as_view(), name='service_order_create'),
    path('service-order/<int:pk>/edit/', views.ServiceOrderUpdateView.as_view(), name='service_order_update'),
    path('service-order/<int:pk>/delete/', views.ServiceOrderDeleteView.as_view(), name='service_order_delete'),
    path('service-order/<int:pk>/toggle-accept/', views.ServiceOrderToggleAcceptView.as_view(), name='service_order_toggle_accept'),

    # Offer
    path('offer/add/', views.OfferCreateView.as_view(), name='offer_create'),
    path('offer/<int:pk>/edit/', views.OfferUpdateView.as_view(), name='offer_update'),
    path('offer/<int:pk>/delete/', views.OfferDeleteView.as_view(), name='offer_delete'),
    path('offer/<int:pk>/select/', views.OfferSelectView.as_view(), name='offer_select'),
    path('offer/<int:pk>/toggle-accept/', views.OfferToggleAcceptView.as_view(), name='offer_toggle_accept'),

    # ChannelPost
    path('post/add/', views.ChannelPostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.ChannelPostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.ChannelPostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/toggle-accept/', views.ChannelPostToggleAcceptView.as_view(), name='post_toggle_accept'),

    # Tender
    path('tenders/', views.TenderListView.as_view(), name='tender_list'),
    path('tender/add/', views.TenderCreateView.as_view(), name='tender_create'),
    path('tender/<int:pk>/edit/', views.TenderUpdateView.as_view(), name='tender_update'),
    path('tender/<int:pk>/delete/', views.TenderDeleteView.as_view(), name='tender_delete'),

    # ATSContract
    path('ats-contract/add/', views.ATSContractCreateView.as_view(), name='ats_contract_create'),
    path('ats-contract/<int:pk>/edit/', views.ATSContractUpdateView.as_view(), name='ats_contract_update'),
    path('ats-contract/<int:pk>/delete/', views.ATSContractDeleteView.as_view(), name='ats_contract_delete'),

    # ContractOperation
    path('contract-operation/add/', views.ContractOperationCreateView.as_view(), name='contract_operation_create'),
    path('contract-operation/<int:pk>/edit/', views.ContractOperationUpdateView.as_view(), name='contract_operation_update'),
    path('contract-operation/<int:pk>/delete/', views.ContractOperationDeleteView.as_view(), name='contract_operation_delete'),
]
