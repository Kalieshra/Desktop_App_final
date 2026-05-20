from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('travel.urls')),
    path('licenses/', include('licenses.urls')),
    path('supplies/', include('supplies.urls')),
    path('investments/', include('investments.urls')),
    path('budgets/', include('budgets.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
