from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
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

    print(cart)

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

def update_product(request, product_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            if action == 'increase':
                cart[str(product_id)]['quantify'] += 1
            elif action == 'decrease':
                if cart[str(product_id)]['quantify'] > 1:
                    cart[str(product_id)]['quantify'] -= 1
                else:
                    return JsonResponse({'error': 'A quantidade mínima é 1'})
        else:
            return JsonResponse({'error': 'Produto não encontrado no carrinho'}, status=404 )
        
        request.session['cart'] = cart
        request.session.modified = True

        subtotal = cart[str(product_id)]['price'] * cart[str(product_id)]['quantify']
        total = sum(item['price'] * item['quantify'] for item in cart.values())

        return JsonResponse({'subtotal': subtotal, 'total': total})
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)