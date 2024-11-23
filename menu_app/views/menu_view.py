from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from menu_app.models import Category, Product
import json


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


def add_to_cart(request, product_id):
    # Obtém o produto específico pelo ID fornecido.
    product = Product.objects.get(pk=product_id)

    # Obtém a quantidade enviada no formulário. Se não for fornecida, usa o valor padrão 1.
    quantity = int(request.POST.get('quantity', 1))

    # Obtém o carrinho atual armazenado na sessão. Se não existir, inicializa como um dicionário vazio.
    cart = request.session.get('cart', {})

    # Verifica se o produto já está no carrinho.
    if str(product.pk) in cart:
        # Se estiver, incrementa a quantidade existente com a nova quantidade.
        cart[str(product.pk)]['quantity'] += quantity
    else:
        # Caso contrário, adiciona o produto ao carrinho com suas informações.
        cart[str(product.pk)] = {
            'name': product.name,  # Nome do produto.
            'price': str(product.price),  # Preço do produto como string.
            'quantity': quantity,  # Quantidade adicionada.
            'image': product.image.url if product.image else '',  # URL da imagem do produto, se existir.
        }

    # Atualiza o carrinho na sessão com as novas informações.
    request.session['cart'] = cart

    # Redireciona o usuário para a página do carrinho.
    return redirect('menu_app:cart')


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


def delete_item(request, product_id):
    # Obtém o carrinho armazenado na sessão. Se não houver, inicializa como um dicionário vazio.
    cart = request.session.get('cart', {})

    # Verifica se o produto identificado pelo 'product_id' existe no carrinho.
    if str(product_id) in cart:
        # Remove o item do carrinho utilizando sua chave (product_id).
        del cart[str(product_id)]

    # Atualiza o carrinho na sessão com a nova lista de itens (sem o item removido).
    request.session['cart'] = cart

    # Redireciona o usuário para a página do carrinho após a remoção do item.
    return redirect('menu_app:cart')

def update_product(request, product_id):
    # Verifica se a requisição é do tipo POST
    if request.method == 'POST':
        try:
            # Tenta carregar os dados recebidos no corpo da requisição como JSON
            data = json.loads(request.body)  # Carregar os dados enviados pelo fetch
            action = data.get('action')  # Obter o valor de 'action'
            print(f"Action received: {action}")  # Depurar o valor recebido
        except json.JSONDecodeError:
            # Se ocorrer um erro ao processar o JSON, retorna uma resposta de erro com status 400 (Bad Request)
            return JsonResponse({'error': 'Erro ao processar JSON'}, status=400)

        # Obtém o carrinho da sessão, ou inicializa como um dicionário vazio se não existir
        cart = request.session.get('cart', {})

        # Verifica se o produto identificado por 'product_id' existe no carrinho
        if str(product_id) in cart:
            # Se a ação for 'increase', aumenta a quantidade do item no carrinho
            if action == 'increase':
                cart[str(product_id)]['quantity'] += 1
            # Se a ação for 'decrease', diminui a quantidade, respeitando o limite mínimo de 1
            elif action == 'decrease':
                if cart[str(product_id)]['quantity'] > 1:
                    cart[str(product_id)]['quantity'] -= 1
                else:
                    # Caso a quantidade seja 1, não permite a diminuição
                    return JsonResponse({'error': 'A quantidade mínima é 1'})
        else:
            # Caso o produto não exista no carrinho, retorna um erro 404
            return JsonResponse({'error': 'Produto não encontrado no carrinho'}, status=404)

        # Atualiza o carrinho na sessão com as alterações feitas
        request.session['cart'] = cart
        request.session.modified = True

        # Calcula a nova quantidade, subtotal e total
        quantity = cart[str(product_id)]['quantity']
        subtotal = (float(cart[str(product_id)]['price']) * cart[str(product_id)]['quantity'])
        total = sum(float(item['price']) * item['quantity'] for item in cart.values())

        # Retorna as informações de subtotal, total e quantidade em formato JSON
        return JsonResponse({'subtotal': subtotal, 'total': total, 'quantity': quantity})

    # Se o método da requisição não for POST, retorna erro 405 (Método não permitido)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def finalize_order_view(request):
    ...

