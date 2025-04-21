from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('secret-admin/', admin.site.urls),
    path('admin/', include('honeypot.urls'), name='honeypot_admin'),
    path('', include('website.urls')),
]
