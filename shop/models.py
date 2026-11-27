from django.db import models
from django.utils.text import slugify


# Create your models here.
class CompanyConfig(models.Model):
    business_name = models.CharField()
    tagline = models.CharField()
    logo = models.ImageField(upload_to="assets/")
    favicon = models.ImageField(upload_to="assets/")
    hero_badge_text = models.CharField()
    hero_title = models.CharField()
    hero_background_image = models.ImageField(upload_to="assets/")
    phone_number = models.CharField()
    whatsapp_number = models.CharField()
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)
    map_latitude = models.DecimalField(max_digits=10, decimal_places=8,
                                       blank=True, null=True)
    map_longitude = models.DecimalField(max_digits=11, decimal_places=8,
                                        blank=True, null=True)
    google_maps_embed_url = models.URLField(blank=True, null=True)


class Category(models.Model):
    name = models.CharField()
    slug = models.SlugField(unique=True, editable=False, blank=True)
    image = models.ImageField(upload_to="cateogry/", blank=True,
                              null=True)
    display_order = models.PositiveIntegerField()
    is_active = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    class BadgeChoice(models.TextChoices):
        NEW_ARRIVAL = "New Arrival", ("New Arrival")
        BULK_DEAL = "Bulk Deal", ("Bulk Deal")
        TRENDING = "Trending", ("Trending")
        BEST_SELLER = "Best Seller", ("Best Seller")

    title = models.CharField()
    slug = models.SlugField(unique=True, editable=False, blank=True)
    sku = models.CharField(db_index=True)
    category = models.ForeignKey(Category, related_name="products",
                                 on_delete=models.CASCADE)
    moq = models.CharField()
    badge = models.CharField(choices=BadgeChoice.choices, blank=True,
                             null=True)
    short_description = models.TextField()
    specifications = models.JSONField()
    is_featured = models.BooleanField()
    is_active = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="images")
    image = models.ImageField(upload_to="products/%Y/%m/")
    alt_text = models.CharField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product.title} - Image {self.id}"
