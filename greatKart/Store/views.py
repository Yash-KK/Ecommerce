from django.shortcuts import render

from Store.models import (
    Product
)
# Create your views here.
def store(request,category_slug=None):
    if category_slug:
        all_products = Product.objects.all().filter(category__slug=category_slug)
        product_count = all_products.count()
    else:    
        all_products = Product.objects.all().filter(is_available=True)
        product_count = all_products.count()
    
    context = {
        'products':all_products, 
        'product_count':product_count
    }
    return render(request,'Store/store.html',context)