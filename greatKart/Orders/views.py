from django.http import HttpResponse
from django.shortcuts import redirect, render

import datetime
# Forms
from .forms import (
    OrderForm
)

# Models
from .models import (
    Order
)
from Cart.models import  (
    CartItem
)

# Create your views here.
def place_order(request):
    current_user = request.user
    
    # If user has no items in the cart, then redirect him to the store page
    cart_items = CartItem.objects.filter(user=current_user)
    cart_items_count = cart_items.count()
    if cart_items_count <= 0:
        return redirect('store')
    tax = 0     
    grand_total = 0
    for item in cart_items:
        total = (item.quantity * item.product.price)
    
    tax = (2*total) /100
    grand_total = tax + total    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_total = grand_total
            data.tax = tax
            data.order_note = form.cleaned_data['order_note']
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()
            
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            
            d = datetime.date(yr,mt,dt)
            current_date  = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'tax': tax,
                'total':total,
                'grand_total':grand_total
            }
            return render(request,'Orders/payments.html',context)
    else:
        return redirect('checkout')        

def payments(request):
    return render(request,'Orders/payments.html')    