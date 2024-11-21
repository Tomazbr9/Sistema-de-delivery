from django.shortcuts import render, get_object_or_404
from menu_app.models import Category, Product


def index(request):
    categorys = Category.objects.all()
    context = {
        'categorys': categorys
    }
    return render(request, 'index.html', context)

def category_by_products_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category_id)
    context = {
        'products': products,
        'category': category
    }
    return render(request, 'products.html', context)

def product_detail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    context = {
            'product': product
    }
    return render(request, 'product.html', context)