from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
