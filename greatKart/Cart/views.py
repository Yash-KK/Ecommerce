from multiprocessing import context

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import (
    login_required
)

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
    cartitem_exist = CartItem.objects.filter(cart=cart,product=product).exists()
        
    if cartitem_exist:
        cart_item = CartItem.objects.filter(product=product,cart=cart)
        
        existing_variations = []
        item_id = []
        for item in cart_item:
            var = item.variations.all()
            existing_variations.append(list(var))
            item_id.append(item.id)          
        
        if product_variation in existing_variations:
            index = existing_variations.index(product_variation)
            _id = item_id[index]
            item = CartItem.objects.get(id=_id,product=product)
            item.quantity +=1
            item.save()
        else:                                                  
            item = CartItem.objects.create(product=product,cart=cart,quantity = 1)            
            if len(product_variation)> 0:
                item.variations.clear()
                item.variations.add(*product_variation)                   
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity = 1,
            cart= cart            
        ) 
        if len(product_variation)> 0:
            cart_item.variations.clear()
            for item in product_variation:                
                cart_item.variations.add(item)       
        cart_item.save()    
    return redirect('cart')    
 
def remove_cartitem(request,product_id,item_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id = _cart_id(request))
    
    cart_item = CartItem.objects.get(product=product,cart=cart,id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()    
    return redirect('cart')        

def delete_cartitem(request,product_id,item_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id = _cart_id(request))
    
    cart_item = CartItem.objects.get(product=product,cart=cart,id=item_id)
    cart_item.delete()
    return redirect('cart')    

# @login_required(login_url='/accounts/login/')
def cart(request,total= 0, cart_items = None, cart=None):
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