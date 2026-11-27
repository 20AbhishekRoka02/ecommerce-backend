from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase, override_settings
from shop.models import Category, CompanyConfig, Product, ProductImage
from shop.serializers import ProductSerializer


class MediaFilesTests(SimpleTestCase):
    def test_media_fields_store_paths_relative_to_media_root(self):
        category = Category(name="Sensors")
        company_config = CompanyConfig()

        self.assertEqual(
            Path(
                Category._meta.get_field("image").generate_filename(
                    category, "sensors.png"
                )
            ).as_posix(),
            "cateogry/sensors.png",
        )
        for field_name in ("logo", "favicon", "hero_background_image"):
            with self.subTest(field=field_name):
                self.assertEqual(
                    Path(
                        CompanyConfig._meta.get_field(
                            field_name
                        ).generate_filename(company_config, "business.png")
                    ).as_posix(),
                    "assets/business.png",
                )

    def test_media_route_serves_files_from_media_root(self):
        with TemporaryDirectory() as media_root:
            image_path = Path(media_root) / "cateogry" / "sensors.png"
            image_path.parent.mkdir()
            image_path.write_bytes(b"test image")

            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.get("/media/cateogry/sensors.png")
                try:
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(
                        b"".join(response.streaming_content), b"test image"
                    )
                finally:
                    response.close()


class ProductSerializerTests(SimpleTestCase):
    def test_product_includes_ordered_image_details(self):
        category = SimpleNamespace(
            id=3,
            name="Sensors",
            slug="sensors",
            image=None,
            display_order=1,
            is_active=True,
        )
        product = SimpleNamespace(
            id=12,
            title="Sensor Module",
            slug="sensor-module",
            sku="SNS-001",
            category=category,
            moq="10 Pcs",
            badge=None,
            short_description="Industrial sensor module",
            specifications={"Output": "4-20mA"},
            is_featured=False,
            is_active=True,
            images=[
                SimpleNamespace(
                    id=21,
                    image=SimpleNamespace(
                        url="http://testserver/media/products/first.png"
                    ),
                    alt_text="Front view",
                    sort_order=0,
                ),
                SimpleNamespace(
                    id=22,
                    image=SimpleNamespace(
                        url="http://testserver/media/products/second.png"
                    ),
                    alt_text="Back view",
                    sort_order=1,
                ),
            ],
        )

        data = ProductSerializer(product).data

        self.assertEqual(len(data["images"]), 2)
        self.assertEqual(data["images"][0]["id"], 21)
        self.assertEqual(
            data["images"][0]["image"],
            "http://testserver/media/products/first.png",
        )
        self.assertEqual(data["images"][0]["alt_text"], "Front view")
        self.assertEqual(data["images"][1]["sort_order"], 1)


class SlugifyOnSaveTests(TestCase):
    def test_category_slug_is_slugified_on_save(self):
        category = Category.objects.create(
            name="Chargers",
            slug="Fast Charge Accessories!",
            display_order=1,
            is_active=True,
        )

        self.assertEqual(category.slug, "fast-charge-accessories")

    def test_product_slug_is_slugified_on_save(self):
        category = Category.objects.create(
            name="Chargers",
            slug="chargers",
            display_order=1,
            is_active=True,
        )
        product = Product.objects.create(
            title="USB-C Charger",
            slug="USB-C 45W Charger!",
            sku="USB-C-45W",
            category=category,
            moq="1",
            short_description="Fast charger",
            specifications={},
            is_featured=False,
            is_active=True,
        )

        self.assertEqual(product.slug, "usb-c-45w-charger")

    def test_slug_is_slugified_when_saving_selected_fields(self):
        category = Category.objects.create(
            name="Chargers",
            slug="chargers",
            display_order=1,
            is_active=True,
        )
        category.slug = "Fast Charge!"
        category.save(update_fields=["name"])
        category.refresh_from_db()

        self.assertEqual(category.slug, "fast-charge")


class SeedSampleDataCommandTests(TestCase):
    def test_seeded_images_are_saved_under_media_root(self):
        with TemporaryDirectory() as directory:
            media_root = Path(directory)
            with override_settings(MEDIA_ROOT=media_root):
                call_command("seed_sample_data", stdout=StringIO())

                config = CompanyConfig.objects.get(pk=1)
                images = [
                    config.logo,
                    config.favicon,
                    config.hero_background_image,
                    *(
                        category.image
                        for category in Category.objects.all()
                    ),
                    *(
                        product_image.image
                        for product_image in ProductImage.objects.all()
                    ),
                ]

                self.assertTrue(images)
                for image in images:
                    image_path = Path(image.path).resolve()
                    self.assertTrue(image_path.is_relative_to(media_root.resolve()))
                    self.assertTrue(image_path.is_file())
