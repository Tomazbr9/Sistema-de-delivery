from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from django.shortcuts import render, redirect, get_object_or_404
from menu_app.models import Customer, Product, Order
from django.http import JsonResponse
from django.template.response import TemplateResponse
from rest_framework.response import Response
from rest_framework import status
from menu_app.serializers import (CustomerSerializer, 
ProductSerializer, OrderSerializer)
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
        
        return Response({'message': 'Item adicionado ao carrinho'})

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
            return Response({'message': 'Item removed successfully'}, status=status.HTTP_200_OK)

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




