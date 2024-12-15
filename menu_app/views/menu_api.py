from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib import messages
from django.shortcuts import redirect
from menu_app.models import Customer, Product, Order, OrderProduct
from menu_app.serializers import (CustomerSerializer, 
ProductSerializer, OrderSerializer)
from decimal import Decimal
import json

# Define a visualização da API para o modelo Customer
class CustomerViewSet(ModelViewSet):
    # Define a queryset (conjunto de objetos) que será retornado pela view
    queryset = Customer.objects.all()  # Recupera todos os objetos do modelo Customer
    # Define o serializer que será usado para transformar os dados do modelo em formato JSON e vice-versa
    serializer_class = CustomerSerializer  # Utiliza o CustomerSerializer para serializar os dados

# Define a visualização da API para o modelo Product
class ProductViewSet(ModelViewSet):
    # Define a queryset (conjunto de objetos) que será retornado pela view
    queryset = Product.objects.all()  # Recupera todos os objetos do modelo Product
    # Define o serializer que será usado para transformar os dados do modelo em formato JSON e vice-versa
    serializer_class = ProductSerializer  # Utiliza o ProductSerializer para serializar os dados

# Define a visualização da API para o modelo Order
class OrderViewSet(ModelViewSet):
    # Define a queryset (conjunto de objetos) que será retornado pela view
    queryset = Order.objects.all()  # Recupera todos os objetos do modelo Order
    # Define o serializer que será usado para transformar os dados do modelo em formato JSON e vice-versa
    serializer_class = OrderSerializer  # Utiliza o OrderSerializer para serializar os dados

class AddToCartView(APIView):
    """
    View para adicionar itens no carrinho
    """
    def post(self, request, product_id):
        # Obter o produto pelo ID
        product = get_object_or_404(Product, pk=product_id)
        
        # Obter a quantidade do corpo da requisição, padrão = 1
        quantity = int(request.data.get('quantity', 1))
        
        # Obter o carrinho da sessão
        cart = request.session.get('cart', {})
        
        # Adicionar ou atualizar o produto no carrinho
        if str(product.pk) in cart:
            cart[str(product.pk)]['quantity'] += quantity
        else:
            cart[str(product.pk)] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': quantity,
                'image': product.image.url if product.image else '',
            }
        
        # Atualizar o carrinho na sessão
        request.session['cart'] = cart
        
        return redirect('menu_app:cart')

class DeleteItemAPIView(APIView):
    """
    APIView para remover um item do carrinho.
    """
    def post(self, request, product_id):
        # Obtém o carrinho armazenado na sessão. Se não houver, inicializa como um dicionário vazio.
        cart = request.session.get('cart', {})

        # Verifica se o produto identificado pelo 'product_id' existe no carrinho.
        if str(product_id) in cart:
            # Remove o item do carrinho utilizando sua chave (product_id).
            del cart[str(product_id)]
            # Atualiza o carrinho na sessão com a nova lista de itens (sem o item removido).
            request.session['cart'] = cart
            return Response({'message': 'Item Removido com sucesso'}, status=status.HTTP_200_OK)

        # Se o item não estiver no carrinho, retorna um erro.
        return Response(
            {'error': 'Item não encontrado no carrinho'}, 
            status=status.HTTP_404_NOT_FOUND
        )

class UpdateItemAPIView(APIView):
    """
    APIView para atualizar a quantidade de um produto no carrinho.
    Permite aumentar ou diminuir a quantidade.
    """
    def post(self, request, product_id):
        try:
            # Tenta carregar os dados do corpo da requisição como JSON
            data = request.data
            action = data.get('action')  # Obtém o valor de 'action'
        except json.JSONDecodeError:
            # Retorna erro se houver falha ao processar o JSON
            return Response({'error': 'Erro ao processar JSON'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtém o carrinho da sessão, ou inicializa como um dicionário vazio
        cart = request.session.get('cart', {})

        # Verifica se o produto existe no carrinho
        if str(product_id) in cart:
            # Se a ação for 'increase', aumenta a quantidade
            if action == 'increase':
                cart[str(product_id)]['quantity'] += 1
            # Se a ação for 'decrease', diminui a quantidade, respeitando o limite mínimo de 1
            elif action == 'decrease':
                if cart[str(product_id)]['quantity'] > 1:
                    cart[str(product_id)]['quantity'] -= 1
                else:
                    return Response({'error': 'A quantidade mínima é 1'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Retorna erro se o produto não for encontrado
            return Response({'error': 'Produto não encontrado no carrinho'}, status=status.HTTP_404_NOT_FOUND)

        # Atualiza o carrinho na sessão com as alterações feitas
        request.session['cart'] = cart
        request.session.modified = True

        # Calcula os valores necessários
        quantity = cart[str(product_id)]['quantity']
        subtotal = float(cart[str(product_id)]['price']) * quantity
        total = sum(float(item['price']) * item['quantity'] for item in cart.values())

        # Retorna as informações atualizadas
        return Response({
            'subtotal': subtotal,
            'total': total,
            'quantity': quantity
        }, status=status.HTTP_200_OK)
    
class FinalizeOrderAPIView(APIView):
    """
    API para finalizar o pedido com os itens do carrinho.
    Cria um pedido com os produtos, quantidades e total.
    """
    def post(self, request):
        # Obtém o carrinho armazenado na sessão
        cart = request.session.get('cart', {})

        # Verifica se o carrinho está vazio
        if not cart:
            return Response({'error': 'O carrinho está vazio'}, status=status.HTTP_400_BAD_REQUEST)

        # Inicializa o total do pedido
        total = 0

        try:
            # Cria o pedido em uma transação atômica
            with transaction.atomic():

                customer = Customer.objects.get(pk=1)
                # customer = get_object_or_404(Customer, pk=customer_id)

                # Cria o objeto do pedido
                order = Order.objects.create(
                    customer = customer
                )

                # Itera pelos itens do carrinho para criar OrderItems
                for product_id, item in cart.items():
                    product = Product.objects.get(pk=product_id)  # Obtém o produto do banco
                    quantity = item['quantity']
                    price = float(item['price'])

                    # Cria um item do pedido
                    OrderProduct.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=price,
                    )

                    # Incrementa o total do pedido
                    total += price * quantity

                # Atualiza o total do pedido
                order.total = Decimal(str(total))
                order.save()

                # Limpa o carrinho da sessão
                request.session['cart'] = {}
                request.session.modified = True

            # Retorna a resposta de sucesso
            return Response({
                'message': 'Pedido finalizado com sucesso!',
                'order_id': order.pk,
                'total': f'{total:.2f}',
                'customer': customer.pk
            }, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({'error': 'Um dos produtos do carrinho não foi encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
