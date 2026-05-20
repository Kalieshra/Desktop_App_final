from django.urls import path
from . import views

app_name = 'investments'

urlpatterns = [
    path('', views.InvestmentPlanListView.as_view(), name='plan_list'),
    path('add/', views.InvestmentPlanCreateView.as_view(), name='plan_create'),
    path('<int:pk>/', views.InvestmentPlanDetailView.as_view(), name='plan_detail'),
    path('<int:pk>/edit/', views.InvestmentPlanUpdateView.as_view(), name='plan_update'),
    path('<int:pk>/delete/', views.InvestmentPlanDeleteView.as_view(), name='plan_delete'),
]
