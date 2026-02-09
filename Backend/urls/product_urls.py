from django.urls import path
from rest_framework.authtoken import views as auth_views
from Backend.views.product_views import *
urlpatterns = [
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/catalog/', ProductCatalogueView.as_view(), name='product_catalogue'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
