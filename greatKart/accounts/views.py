from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
)

# VERIFICATION
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
 

from .models import (
    Account
)

from .forms import (
    RegisterForm
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
                auth_login(request,user)
                messages.success(request,"User Logged in Successfully!")
                return redirect('dashboard')            
        else:
            messages.error(request,'Login not Successfull! Please try Again!')
            return redirect("login")
    return render(request,'accounts/login.html')

def logout(request):
    messages.success(request,'Logged Out Successfully!')
    auth_logout(request)     
    return redirect('login')

def dashboard(request):
    return render(request,'accounts/dashboard.html')