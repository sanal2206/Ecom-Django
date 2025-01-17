from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from PIL import Image
import datetime
from django_resized import ResizedImageField


# Category of products
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


# userss
class CustomUser(AbstractUser):
    # Add custom fields here
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username 

# Products
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    Brand = models.CharField(max_length=50,default='')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1,related_name="products")
    description = models.TextField(default='', blank=True, null=True)
    thumbnail = ResizedImageField(upload_to='uploads/product/', size=[300, 250], default='uploads/product/lap.jpg',crop=['middle', 'center'], force_format='JPEG')
 
     

    def __str__(self):
        return self.name

  

# Product Images
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = ResizedImageField(upload_to='uploads/product_images/',  size=[300, 250],crop=['middle', 'center'], force_format='JPEG')


    
    def __str__(self):
        return f"Image for {self.product.name}"

#Review
 
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField(blank=True)  # Detailed review text
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the review is created

    def __str__(self):
        return f"Review by {self.user.first_name} for {self.product.name}"


# # Customer Orders
# class Order(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     address = models.CharField(max_length=200, default='', blank=True)
#     phone = models.CharField(max_length=20, default='', blank=True)
#     date = models.DateField(default=datetime.date.today)
#     status = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Order of {self.product.name} by {self.user.first_name} {self.user.last_name}"
