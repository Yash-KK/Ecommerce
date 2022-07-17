from django.urls import path
from . import views

urlpatterns = [
    path("",views.cart,name='cart'),
    path("addtocart/<int:product_id>/",views.addto_cart,name='add-to-cart'),
    path("checkout/",views.checkout,name='checkout'),
    path("removecartitem/<int:product_id>/<int:item_id>/",views.remove_cartitem,name='remove-cartitem'),
    path("delete_cartitem/<int:product_id>/<int:item_id>/",views.delete_cartitem,name='delete-cartitem')
]
