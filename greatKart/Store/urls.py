from django.urls import path

from . import views

urlpatterns = [
    path("",views.store,name='s-store'),
    path("<slug:category_slug>/",views.store,name='products-by-category')
]
