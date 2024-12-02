from django.contrib import admin
from .models import Category, Product, ProductImage,  Review,CustomUser

from django.utils.html import format_html  # Import format_html (if needed)

# Inline admin for product images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Number of extra image upload fields

# Admin configuration for Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category','thumbnail')  # Display fields
    search_fields = ('name', 'description')  # Add a search box for these fields
    list_filter = ('category', 'price')  # Filters on the right sidebar
    ordering = ('-price',)  # Default ordering by price (descending)
    inlines = [ProductImageInline]  # Inline images

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Customize the list display and add fields as needed
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=['id','user','product','rating','created_at']
    readonly_fields=['created_at']
    ordering=['-created_at']




# Register your models here
admin.site.register(Product, ProductAdmin)  # Register Product with its custom admin
admin.site.register(Category)  # Register Category model
admin.site.register(ProductImage) 
 
 