from rest_framework.viewsets import ModelViewSet
from menu_app.models import Customer, Product, Order
from menu_app.serializers import (CustomerSerializer, 
ProductSerializer, OrderSerializer)

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

