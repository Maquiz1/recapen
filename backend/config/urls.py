"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboards.urls')),
    path('patients/', include('patients.urls')),
    path('laboratory/', include('laboratory.urls')),
    path('radiology/', include('radiology.urls')),
    path('cardiology/', include('cardiology.urls')),
    path('encounters/', include('encounters.urls')),
    path('orders/', include('orders.urls')),
    path('medications/', include('medications.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('appointments/', include('appointments.urls')),
    path('documents/', include('documents.urls')),
    path('audit/', include('audit.urls')),
    path('study-config/', include('study_config.urls')),
    path('encounters/', include('encounters.urls')),
    path('clinical/', include('clinical.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
