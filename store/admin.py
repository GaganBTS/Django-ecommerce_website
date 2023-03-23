from django.contrib import admin

# Register your models here.
from .models import Category, Product, Wishlist, Reviews

# Register your models here.
admin.site.register(Wishlist)
admin.site.register(Reviews)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
