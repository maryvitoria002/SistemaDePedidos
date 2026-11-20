from django.urls import path
from . import views

urlpatterns = [
    path('', views.cliente_list, name='cliente-list'),
    path('<uuid:id>/', views.get_by_id, name='cliente-detail'),
    path('create/', views.create_cliente, name='cliente-create'),
    path('<uuid:id>/update/', views.update_cliente, name='cliente-update'),
    path('<uuid:id>/delete/', views.delete_cliente, name='cliente-delete'),
    path('<uuid:id>/pedidos/', views.cliente_pedidos, name='cliente-pedidos'),
]