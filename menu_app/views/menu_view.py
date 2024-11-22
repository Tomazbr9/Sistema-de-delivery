from django.shortcuts import render, get_object_or_404, redirect
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

def add_to_cart(request, product_id):
    
    product = Product.objects.get(pk=product_id)

    quantify = int(request.POST.get('quantify', 1))

    cart = request.session.get('cart', {})

    if str(product.pk) in cart:
        cart[str(product.pk)]['quantify'] += quantify
    else:
        cart[str(product.pk)] = {
            'name': product.name,
            'price': str(product.price),
            'quantify': quantify,
            'image': product.image.url if product.image else '',
        }
    
    request.session['cart'] = cart

    return redirect('menu_app:cart')

def view_cart(request):

    cart = request.session.get('cart', {})
    total = 0
    for item in cart.values():
        total += float(item['price']) * item['quantify']
    
    context = {
        'cart': cart,
        'total': total
    }

    return render(request, 'cart.html', context)

def delete_item(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
   
    return redirect('menu_app:cart')

def check(request):
    ...