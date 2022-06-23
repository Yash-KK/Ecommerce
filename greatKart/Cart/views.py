from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render

from Store.models import (
    Product,
    Variation
)
from .models import (
    Cart,
    CartItem
)
# Create your views here.

def _cart_id(request):  # Session key
    cart =request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart   
    

def addto_cart(request,product_id):
    product = Product.objects.get(id=product_id)  # Get the Product
    product_variation = []
    if request.method == 'POST':        
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass                                
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))            # Get the Cart    
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)                               # if Cart not available, Create the cart
        )    
        cart.save()    
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity = 1,
            cart= cart            
        )        
        cart_item.save()    
    return redirect('cart')    

def remove_cartitem(request,product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id = _cart_id(request))
    
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()    
    return redirect('cart')        

def delete_cartitem(request,product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id = _cart_id(request))
    
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')    

def cart(request,total= 0, cart_items = None):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    cart_items = CartItem.objects.filter(cart = cart, is_active = True)
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
    
    tax = (2*total)/100
    grand_total = tax + total
        
    context = {
        'cart_items':cart_items,
        'total': total,
        'tax':tax,
        "grand_total":grand_total
    }
    return render(request,'Cart/cart.html',context)