from django.urls import path
from .api_views import pedidos_list

urlpatterns = [
    path('pedidos/', pedidos_list, name='api_pedidos'),
]
