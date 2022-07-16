from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from Store.models import (
    Product
)


def home(request):
    all_products = Product.objects.all().filter(is_available=True)
    context = {
        'products':all_products
    }
    return render(request,'home.html',context)

