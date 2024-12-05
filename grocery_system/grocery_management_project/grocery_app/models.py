from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class data(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)

    def __str__(self):
        return self.username

class category(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product/')
    description = models.TextField()
    price = models.FloatField()
    carousal_image=models.ImageField(upload_to='product/',default='photo')
    category=models.ForeignKey(category,on_delete=models.CASCADE,default="fruits")

    def __str__(self):
        return self.product_name
    
      
class CartItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price=models.FloatField(default=0)
    total_item=models.IntegerField(default=0)
    quantity=models.IntegerField(default=0)
    total_price=models.FloatField(default=0)
    ordered=models.BooleanField(default=False)

    def __str__(self):
        return self.product.product_name

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    # Add more fields as needed (e.g., status, payment info)

    def __str__(self):
        return self.product.product_name
    


    


 





