from django.contrib import admin

from .models import (
    Product
) 
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','product_name','p_slug','category','is_available']
    list_display_links = ['id','product_name']
    prepopulated_fields = {'p_slug': ('product_name',)} # new
    
admin.site.register(Product,ProductAdmin)                 

 