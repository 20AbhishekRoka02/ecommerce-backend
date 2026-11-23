from django.contrib import admin
from shop.models import CompanyConfig, Category, Product

class CompanyConfigAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_phone_number')

    def has_add_permission(self, request):
        return not CompanyConfig.objects.exists()
    
    def has_delete_permission(self, request, obj = ...):
        return False

    

# Register your models here.
admin.site.register(CompanyConfig, CompanyConfigAdmin)
admin.site.register(Category)
admin.site.register(Product)