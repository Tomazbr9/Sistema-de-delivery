from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categorys/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

# Tabela de Produto
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

# Tabela de Endereço multivalorada
class Address(models.Model):
    full_address = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    complement = models.CharField(max_length=255, blank=True, null=True)
    name_address = models.CharField(max_length=20, blank=True, null=True)
    reference = models.CharField(max_length=255)

    def __str__(self):
        return self.full_address
    
    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

# Tabela de Cliente
class Customer(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    

# Tabela de Pedidos
class Order(models.Model):
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('producao', 'Produção'),
        ('enviado', 'Enviado'),
        ('concluido', 'Concluido'),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='pedidos'
    )
    products = models.ManyToManyField(Product)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pendente'
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido: {self.pk} - {self.customer.name}'
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
