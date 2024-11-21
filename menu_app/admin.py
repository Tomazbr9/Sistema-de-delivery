from django.contrib import admin
from .models import Product, Address, Customer, Order, Category

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
    list_display = ['id', 'customer', 'total', 'status', 'date']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']


