
from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static
from mainApp.api import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.catalogo, name="catalogo"),
    path("producto/<slug:slug>/", views.detalle_producto, name="producto_detalle"),
    path("solicitar/<int:producto_id>/", views.solicitud_producto, name="solicitud_producto"),
    path("seguimiento/<str:token>/", views.seguimiento_pedido, name="seguimiento_pedido"),
    path('api/insumos/', api_views.insumo_list, name='insumo_list'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

