from posixpath import split
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
)
from urllib.parse import urlparse
# VERIFICATION
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Models
from .models import (
    Account
) 
from Cart.models import (
    Cart,
    CartItem
)

# Forms
from .forms import (
    RegisterForm
)

# Views
from Cart.views import (
    _cart_id
)
# Write your views here
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            
            
            # USER VERIFICATION
            current_site = get_current_site(request)
            mail_sibject = 'Please Activate your Account'
            message = render_to_string('accounts/accounts_verification.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            
            to_email = email
            send_email = EmailMessage(mail_sibject,message,to=[to_email])
            send_email.send()
            
            messages.success(request,'Thank You for Registering! We have sent a Verification Email to your email Address')
            return redirect("/accounts/login/?=verification&email="+ email)
        else:
            messages.error(request,'Registeration Unsuccessfull')
            return redirect('register') 
    else:
        form = RegisterForm()            
        
    context = {
        'form':form,
    }
    return render(request,'accounts/register.html',context)


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Congrajulations! Your Account has been activated!')
        return redirect('login')
    else:
        messages.error(request,'Invalid Activation Link!')
        return redirect('register')    
            

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cartitem_exist = CartItem.objects.filter(cart=cart).exists()  
                if cartitem_exist:
                    cart_items = CartItem.objects.filter(cart=cart)
                    
                    # For the existing cart
                    product_variations = []
                    for item in cart_items:
                        var = item.variations.all()
                        product_variations.append(list(var))
                    
                    # For the Current Cart id (woh cart id wala items jab user click karta hai login ko)
                    cart_item = CartItem.objects.filter(user=user)            
                    existing_variations = []
                    item_id = []
                    for item in cart_item:
                        var = item.variations.all()
                        existing_variations.append(list(var))
                        item_id.append(item.id)  
                    
                    for pr in product_variations:
                        if pr in existing_variations:   # If that pro_var is in existing product variations, then increment the item
                            index = existing_variations.index(pr)
                            i_id = item_id[index]
                            item = CartItem.objects.get(id=i_id)
                            item.quantity +=1
                            item.user = user
                            item.save()
                        else:
                            cart_items = CartItem.objects.filter(cart=cart)         
                            for item in cart_items:
                                item.user = user
                                item.save()                    
            except:
                pass                      
            auth_login(request,user)
            messages.success(request,"User Logged in Successfully!")
            url = request.META.get('HTTP_REFERER')
            try:
                query = urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:                
                return redirect('dashboard')            
        else:
            messages.error(request,'Login not Successfull! Please try Again!')
            return redirect("login")
    return render(request,'accounts/login.html')

def logout(request):
    messages.success(request,'Logged Out Successfully!')
    auth_logout(request)     
    return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            
            user = Account.objects.get(email=email)            
            current_site = get_current_site(request)
            mail_sibject = 'Please Activate your Account'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            
            to_email = email
            send_email = EmailMessage(mail_sibject,message,to=[to_email])
            send_email.send()
            messages.success(request,'email to reset your password has been sent!')
            return redirect('login')
        else:
            messages.error(request,'Email does not exist!')
            return redirect('forgot-password')
    return render(request,'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'Reset your Password')
        return redirect('reset-password')
    else:
        messages.error(request,'Link has been expired!')
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(id=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset Successfull')
            return redirect('login')
        else:
            messages.error(request,'Password do not match!')
            return redirect('reset-password')
    else:    
        return render(request,'accounts/reset_password.html')

def dashboard(request):
    return render(request,'accounts/dashboard.html')