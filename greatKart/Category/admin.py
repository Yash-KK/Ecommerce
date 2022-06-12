from django.contrib import admin
from .models import (
    Category
)
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','category_name','slug']
    list_display_links = ['id','category_name']
    prepopulated_fields = {'slug': ('category_name',)} # new
    
admin.site.register(Category,CategoryAdmin)

