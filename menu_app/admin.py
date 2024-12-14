from django.contrib import admin
from .models import Product, Address, Customer, Order, Category, OrderProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'available']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['full_address', 'number', 'complement', 'reference', 'name_address']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'address']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total', 'status', 'created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity', 'price']




