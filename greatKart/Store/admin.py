from django.contrib import admin

from .models import (
    Product,
    Variation
) 
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','product_name','p_slug','category','is_available']
    list_display_links = ['id','product_name']
    prepopulated_fields = {'p_slug': ('product_name',)} # new
 
class VariationAdmin(admin.ModelAdmin):
    list_display = ('id','product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')
    # list_ordering = ('-id',)
        
admin.site.register(Product,ProductAdmin)                 
admin.site.register(Variation,VariationAdmin)
 