# your_project/urls.py

from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static,settings# Correct import here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('waterbodies_app.urls')),
    # Add other URLs for your project.
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
