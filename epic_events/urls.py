from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('', include('crm.urls')),
    path('login/', views.obtain_auth_token),
    path('admin/', admin.site.urls),
]
