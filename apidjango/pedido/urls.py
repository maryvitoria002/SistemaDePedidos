from django.urls import path
from . import views

urlpatterns = [
    path('', views.pedido_list, name='pedido-list'),
    path('<uuid:id>/', views.get_by_id, name='pedido-detail'),
    path('create/', views.create_pedido, name='pedido-create'),
    path('<uuid:id>/update/', views.update_pedido, name='pedido-update'),
    path('<uuid:id>/delete/', views.delete_pedido, name='pedido-delete'),
    path('<uuid:id>/pagar/', views.pagar_pedido, name='pedido-pagar'),
    path('<uuid:id>/cancelar/', views.cancelar_pedido, name='pedido-cancelar'),
]