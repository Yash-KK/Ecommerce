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

variation_category_choices = (
    ('color','color'), 
    ('size','size'),
)    

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size')
    
    
class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=variation_category_choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    objects = VariationManager()
    def __str__(self):
        return f"{self.variation_value}"
    