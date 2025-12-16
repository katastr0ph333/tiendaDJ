from django.contrib import admin
from django.urls import include, path
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static
from mainApp.api import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainApp.urls')),
    




] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

