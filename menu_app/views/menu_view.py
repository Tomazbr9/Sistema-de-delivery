from django.shortcuts import render, get_object_or_404, redirect
from menu_app.models import Category, Product, OrderProduct, Order, Customer
from menu_app.forms import LoginForm

def index(request):
    # Obtém todas as categorias do banco de dados usando o modelo Category.
    categorys = Category.objects.all()
    
    # Cria um dicionário de contexto com as categorias, para enviar para o template.
    context = {
        'categorys': categorys  # Passa as categorias para serem exibidas no template.
    }
    
    # Renderiza o template 'index.html', passando o contexto com as categorias.
    return render(request, 'index.html', context)


def category_by_products_view(request, category_id):
    # Tenta obter uma categoria específica pelo ID fornecido.
    # Se a categoria não for encontrada, retorna uma página 404.
    category = get_object_or_404(Category, pk=category_id)
    
    # Filtra os produtos que pertencem à categoria selecionada.
    products = Product.objects.filter(category=category_id)
    
    # Cria um dicionário de contexto com os produtos e a categoria para enviar ao template.
    context = {
        'products': products,  # Lista de produtos da categoria selecionada.
        'category': category   # Detalhes da categoria selecionada.
    }
    
    # Renderiza o template 'products.html', passando o contexto com os produtos e a categoria.
    return render(request, 'products.html', context)


def product_detail(request, product_id):
    # Tenta obter um produto específico pelo ID fornecido.
    # Se o produto não for encontrado, retorna uma página 404.
    product = get_object_or_404(Product, pk=product_id)
    
    # Cria um dicionário de contexto com o produto para enviar ao template.
    context = {
        'product': product  # Detalhes do produto selecionado.
    }
    
    # Renderiza o template 'product.html', passando o contexto com os detalhes do produto.
    return render(request, 'product.html', context)


def view_cart(request):
    # Obtém o carrinho armazenado na sessão. Se não houver, inicializa como um dicionário vazio.
    cart = request.session.get('cart', {})

    # Calcula o valor total do carrinho.
    total = 0
    for item in cart.values():
        # Para cada item no carrinho, multiplica o preço pela quantidade e soma ao total.
        total += float(item['price']) * item['quantity']

    # Prepara o contexto com o carrinho e o total calculado para enviar ao template.
    context = {
        'cart': cart,  # Carrinho com os itens e suas informações.
        'total': total  # Total acumulado do carrinho.
    }

    # Renderiza o template 'cart.html', passando o contexto com os dados do carrinho.
    return render(request, 'cart.html', context)

def wish_list_view(request):

    customer = Customer.objects.get(pk=1)

    orders = Order.objects.filter(
        customer=customer).prefetch_related('order_products__product')
    
    context = {
        'orders': orders
    }
    
    return render(request, 'wish_list.html', context)

def register_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(...)
    else:
        form = LoginForm()

    context = {
        'form' : form
    }

    return render(request, 'register.html', context)
        
    