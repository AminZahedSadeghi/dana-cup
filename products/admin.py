from django.contrib import admin

from .models import Product, Category, ProductColor
from django.contrib.humanize.templatetags.humanize import intcomma


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'show_price', 'is_discount']
    filter_horizontal = ['colors']
    search_fields = ['title']
    search_help_text = 'You can search with title'

    @admin.display(ordering='discount_price', description='price')
    def show_price(self, o):
        return intcomma(o.discount_price)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
