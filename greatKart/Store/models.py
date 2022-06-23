from django.db import models
from Category.models import Category
from django.urls import reverse
# Create your models here.
 
class Product(models.Model):
    product_name = models.CharField(max_length=100,unique=True)
    p_slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=500)
    pro_images = models.ImageField(upload_to='photo/Products/') 
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)  
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def product_url(self):
        return reverse('product-detail',args=[self.category.slug,self.p_slug])        
     
    def __str__(self):
        return f"{self.product_name}" 