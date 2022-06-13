from msilib.schema import Error
from django.http import HttpResponse
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

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,p_slug=product_slug)
    except Exception as Error:
        raise Error  
    context = {
        'single_product':single_product
    }
    return render(request,'Store/product_detail.html',context)