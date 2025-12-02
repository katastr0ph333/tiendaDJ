
from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.catalogo_producto, name="catalogo_home"),
    path("producto/<slug:slug>/", views.detalle_producto, name="detalle_producto"),
    path("solicitar/<int:producto_id>/", views.solicitud_pedido, name="solicitud_pedido_base"),
    path("solicitar/<int:producto_id>/", views.solicitud_pedido, name="solicitud_pedido_producto"),
    path("seguimiento/<str:token>/", views.seguimiento_pedido, name="seguimiento_detalle"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

