from django.db import models

# Create your models here.
class CompanyConfig(models.Model):
    company_name = models.CharField()
    company_logo = models.ImageField(upload_to="media/assets/")
    company_tagline = models.CharField()
    company_address = models.TextField()
    company_phone_number = models.CharField()
    company_whatsapp = models.CharField()
    company_email = models.EmailField()


class Category(models.Model):
    name = models.CharField()
    image = models.ImageField(upload_to="media/cateogry/", blank=True, null=True)
    priority = models.IntegerField()

class Product(models.Model):
    name = models.CharField()
    description = models.TextField()
    main_image = models.ImageField(upload_to="media/product/")
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    