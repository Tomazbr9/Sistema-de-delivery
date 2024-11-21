from django.urls import path
from menu_app import views

app_name = 'menu_app'

urlpatterns = [
    path('menu/', views.index, name='menu'),
    path('category/<int:category_id>/', views.category_by_products_view, name='category'),
    path('product/<int:product_id>/', views.product_detail, name='product')
]
