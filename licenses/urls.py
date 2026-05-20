from django.urls import path
from . import views

app_name = 'licenses'

urlpatterns = [
    # Channel
    path('', views.ChannelListView.as_view(), name='channel_list'),
    path('channel/add/', views.ChannelCreateView.as_view(), name='channel_create'),
    path('channel/<int:pk>/', views.ChannelDetailView.as_view(), name='channel_detail'),
    path('channel/<int:pk>/edit/', views.ChannelUpdateView.as_view(), name='channel_update'),
    path('channel/<int:pk>/delete/', views.ChannelDeleteView.as_view(), name='channel_delete'),
    path('channel/<int:pk>/toggle-accept/', views.ChannelToggleAcceptView.as_view(), name='channel_toggle_accept'),

    # PlaceLicense
    path('place-license/add/', views.PlaceLicenseCreateView.as_view(), name='place_license_create'),
    path('place-license/<int:pk>/edit/', views.PlaceLicenseUpdateView.as_view(), name='place_license_update'),
    path('place-license/<int:pk>/delete/', views.PlaceLicenseDeleteView.as_view(), name='place_license_delete'),
    path('place-license/<int:pk>/toggle-accept/', views.PlaceLicenseToggleAcceptView.as_view(), name='place_license_toggle_accept'),

    # PersonalLicense
    path('personal-license/add/', views.PersonalLicenseCreateView.as_view(), name='personal_license_create'),
    path('personal-license/<int:pk>/edit/', views.PersonalLicenseUpdateView.as_view(), name='personal_license_update'),
    path('personal-license/<int:pk>/delete/', views.PersonalLicenseDeleteView.as_view(), name='personal_license_delete'),
    path('personal-license/<int:pk>/toggle-accept/', views.PersonalLicenseToggleAcceptView.as_view(), name='personal_license_toggle_accept'),

    # Inspection
    path('inspection/add/', views.InspectionCreateView.as_view(), name='inspection_create'),
    path('inspection/<int:pk>/edit/', views.InspectionUpdateView.as_view(), name='inspection_update'),
    path('inspection/<int:pk>/delete/', views.InspectionDeleteView.as_view(), name='inspection_delete'),
    path('inspection/<int:pk>/toggle-accept/', views.InspectionToggleAcceptView.as_view(), name='inspection_toggle_accept'),
]
