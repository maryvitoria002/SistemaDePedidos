from django.urls import path
from . import views

urlpatterns = [
    path('', views.produto_list, name='produto-list'),
    path('<uuid:id>/', views.get_by_id, name='produto-detail'),
    path('<uuid:id>/update/', views.update_produto, name='produto-update'),
    path('create/', views.create_produto, name='produto-create'),
    path('<uuid:id>/delete/', views.delete_produto, name='produto-delete')
]
