from django.urls import path
from menu_app import views

app_name = 'menu_app'

urlpatterns = [
    path('menu/', views.index, name='menu'),
    path('category/<int:category_id>/', views.category_by_products_view, name='category'),
    path('product/<int:product_id>/', views.product_detail, name='product'),
    path('cart/', views.view_cart, name='cart'),


    # path('cart/update/<int:product_id>/', views.update_product, name='update_product'),
    path('add_item/<int:product_id>/', views.AddToCartView.as_view(), name='add_item'),
    path('remove_item/<int:product_id>/', views.DeleteItemAPIView.as_view(), name='remove_item'),
    path('update_item/<int:product_id>/', views.UpdateItemAPIView.as_view(), name='update_item'),
    path('finalize_order/', views.FinalizeOrderAPIView.as_view(), name='finalize_order')
]
