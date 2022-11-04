from django.contrib import admin

from .models import Category, Product, ProductImage, Tag, Comment

admin.site.register((Tag, Comment))

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class TabularInLineImages(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated', 'tag']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TabularInLineImages]

admin.site.register(Product, CategoryAdmin)