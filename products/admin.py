from django.contrib import admin

# Register your models here.

from .models import Product, ProductImage, Category

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 0
	max_num = 10

class ProductAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'price']
	inlines = [
		ProductImageInline,
	]
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)

admin.site.register(Category)