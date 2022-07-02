from itertools import product
from msilib.schema import Error
from django.http import HttpResponse
from django.shortcuts import render

# Paginator
from django.core.paginator import Paginator

from Store.models import (
    Product
)
from Cart.models import (
    Cart, 
    CartItem
)
from Cart.views import _cart_id
# Create your views here.
def store(request,category_slug=None):    
    if category_slug:
        all_products = Product.objects.all().filter(category__slug=category_slug).order_by('id')
        product_count = all_products.count()
        paginator = Paginator(all_products,1)
        page = request.GET.get('page',1)
        paged_products = paginator.page(page)
    else:    
        all_products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(all_products,6)
        page = request.GET.get('page',1)
        paged_products = paginator.page(page)
        product_count = all_products.count() 
     
    context = {
        # 'products':all_products, 
        'products':paged_products, 
        'product_count':product_count
    }
    return render(request,'Store/store.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:              
            products = Product.objects.filter(category__category_name=keyword)   
            p_count = products.count()         
    context = {
        'products':products,
        'product_count':p_count
    }            
    return render(request,'Store/store.html',context) 
  
def product_detail(request,category_slug,product_slug):    
    
    try:
        single_product = Product.objects.get(category__slug=category_slug,p_slug=product_slug)
        cart_item = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as Error:
        raise Error  
    context = {
        'single_product':single_product,
        'cart_item':cart_item
    } 
    return render(request,'Store/product_detail.html',context)