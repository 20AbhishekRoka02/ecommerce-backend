from django.contrib import admin
from shop.models import CompanyConfig, Category, Product, ProductImage


class CompanyConfigAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'phone_number')

    def has_add_permission(self, request):
        return not CompanyConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "badge", "is_featured", "is_active"]
    inlines = [ProductImageInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "display_order", "is_active"]


# Register your models here.
admin.site.register(CompanyConfig, CompanyConfigAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)