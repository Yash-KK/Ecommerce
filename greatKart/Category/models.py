from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=200,blank=True)
    image = models.ImageField(upload_to='photo/categories/')
    
    class Meta: 
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self): 
        return f"{self.category_name}"
     