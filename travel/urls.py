from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.TravelListView.as_view(), name='list'),
    path('by-person/', views.TravelByPersonListView.as_view(), name='by_person'),
    path('<int:pk>/', views.TravelDetailView.as_view(), name='detail'),
    path('add/', views.TravelCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TravelUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TravelDeleteView.as_view(), name='delete'),
    path('<int:pk>/toggle-accept/', views.TravelToggleAcceptView.as_view(), name='toggle_accept'),
    path('import/', views.import_excel, name='import'),
    path('backup/', views.backup_all, name='backup'),

    # TravelType CRUD
    path('travel-type/', views.TravelTypeListView.as_view(), name='travel_type_list'),
    path('travel-type/add/', views.TravelTypeCreateView.as_view(), name='travel_type_create'),
    path('travel-type/<int:pk>/', views.TravelTypeDetailView.as_view(), name='travel_type_detail'),
    path('travel-type/<int:pk>/edit/', views.TravelTypeUpdateView.as_view(), name='travel_type_update'),
    path('travel-type/<int:pk>/delete/', views.TravelTypeDeleteView.as_view(), name='travel_type_delete'),
]
