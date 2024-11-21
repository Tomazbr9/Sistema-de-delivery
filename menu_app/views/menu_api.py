from rest_framework.viewsets import ModelViewSet
from menu_app.models import Customer, Product, Order
from menu_app.serializers import (CustomerSerializer, 
ProductSerializer, OrderSerializer)

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
