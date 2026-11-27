import io
from pathlib import Path

from PIL import Image, ImageDraw
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from shop.models import CompanyConfig, Category, Product, ProductImage


def make_placeholder_image(label: str, bg_color: tuple, size=(800, 600)) -> ContentFile:
    """Generates a valid PNG in memory for required ImageFields."""
    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)
    w, h = size
    draw.rectangle([20, 20, w - 20, h - 20], outline=(255, 255, 255), width=3)
    draw.text((40, h // 2 - 10), label, fill=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return ContentFile(buf.getvalue())


class Command(BaseCommand):
    help = "Seeds sample CompanyConfig, Category, Product, and ProductImage records."

    @transaction.atomic
    def handle(self, *args, **options):
        Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)

        # 1. CompanyConfig (Singleton)
        config, _ = CompanyConfig.objects.get_or_create(
            id=1,
            defaults={
                "business_name": "IR Electronics",
                "tagline": "Innovative Technology... Better Tomorrow",
                "hero_badge_text": "B2B Wholesale Electronics Supplier",
                "hero_title": "Bulk Electronic Components & Industrial Hardware",
                "phone_number": "+919968189924",
                "whatsapp_number": "+919968189924",
                "email": "",
                "address": None,
                "map_latitude": None,
                "map_longitude": None,
                "google_maps_embed_url": None,
            },
        )
        if not config.logo:
            config.logo.save("ir-logo.png", make_placeholder_image("IR Electronics", (11, 34, 83), (400, 140)), save=False)
        if not config.favicon:
            config.favicon.save("ir-favicon.png", make_placeholder_image("IR", (227, 6, 19), (64, 64)), save=False)
        if not config.hero_background_image:
            config.hero_background_image.save("ir-hero-bg.png", make_placeholder_image("IR Electronics Wholesale", (10, 59, 140), (1376, 768)), save=False)
        config.save()

        # 2. Categories
        categories_data = [
            {"name": "Power Supplies", "display_order": 1, "color": (11, 34, 83)},
            {"name": "Microcontrollers & ICs", "display_order": 2, "color": (15, 76, 129)},
            {"name": "Cables & Connectors", "display_order": 3, "color": (30, 41, 59)},
            {"name": "Industrial Automation", "display_order": 4, "color": (127, 29, 29)},
            {"name": "Sensors & Modules", "display_order": 5, "color": (6, 78, 59)},
        ]

        cat_map = {}
        for item in categories_data:
            cat, _ = Category.objects.update_or_create(
                name=item["name"],
                defaults={
                    "display_order": item["display_order"],
                    "is_active": True,
                },
            )
            if not cat.image:
                cat.image.save(
                    f"{cat.slug}.png",
                    make_placeholder_image(cat.name, item["color"], (400, 400)),
                    save=True,
                )
            cat_map[item["name"]] = cat

        # 3. Products (using exact Product.BadgeChoice values)
        products_data = [
            {
                "title": "24V 10A Industrial SMPS Switching Power Supply",
                "sku": "IR-SMPS-2410",
                "category": "Power Supplies",
                "moq": "25 Units",
                "badge": Product.BadgeChoice.BULK_DEAL,
                "is_featured": True,
                "short_description": "Heavy-duty perforated metal chassis SMPS with overload, over-voltage, and short-circuit protection.",
                "specifications": {"Input Voltage": "180-264V AC", "Output": "24V DC / 10A (240W)", "Cooling": "Natural Convection", "Certification": "CE / RoHS"},
                "color": (11, 34, 83),
            },
            {
                "title": "12V 20A DIN-Rail Regulated Power Module",
                "sku": "IR-PSU-1220",
                "category": "Power Supplies",
                "moq": "20 Units",
                "badge": Product.BadgeChoice.TRENDING,
                "is_featured": True,
                "short_description": "Compact industrial control cabinet power supply engineered for 24/7 PLC and automation panels.",
                "specifications": {"Output": "12V DC / 20A", "Efficiency": "89% Typical", "Mounting": "DIN-Rail", "Protection": "OVP, OCP, OTP"},
                "color": (10, 59, 140),
            },
            {
                "title": "STM32F4 ARM Cortex-M4 Development & IC Kit",
                "sku": "IR-MCU-407",
                "category": "Microcontrollers & ICs",
                "moq": "50 Pcs",
                "badge": Product.BadgeChoice.NEW_ARRIVAL,
                "is_featured": True,
                "short_description": "High-speed 32-bit microcontroller boards and SMD IC trays for OEM embedded manufacturing.",
                "specifications": {"Core": "ARM Cortex-M4 168MHz", "Memory": "1MB Flash / 192KB RAM", "Interfaces": "USB, CAN, SPI, I2C", "Package": "LQFP-100 / Tray"},
                "color": (15, 76, 129),
            },
            {
                "title": "ATmega328P & Logic Gate Bulk IC Lot",
                "sku": "IR-IC-328P",
                "category": "Microcontrollers & ICs",
                "moq": "200 Pcs",
                "badge": Product.BadgeChoice.BULK_DEAL,
                "is_featured": False,
                "short_description": "Factory-sealed anti-static tube and reel IC lots for high-volume PCB assembly lines.",
                "specifications": {"Operating Voltage": "1.8V - 5.5V", "Clock": "Up to 20MHz", "Temp Range": "-40C to +85C", "Packaging": "ESD Safe Tubes"},
                "color": (25, 55, 109),
            },
            {
                "title": "GX16 4-Pin Shielded Aviation Control Cable (2m)",
                "sku": "IR-CBL-GX16",
                "category": "Cables & Connectors",
                "moq": "100 Pcs",
                "badge": Product.BadgeChoice.BEST_SELLER,
                "is_featured": True,
                "short_description": "Braided copper-shielded 2x0.75mm2 industrial cable with nickel-plated threaded aviation connectors.",
                "specifications": {"Connector": "GX16 4-Pin Metal", "Conductor": "Oxygen-Free Copper", "Shielding": "Braided EMI Shield", "Rating": "300V / 5A"},
                "color": (30, 41, 59),
            },
            {
                "title": "Heavy-Duty RS485 Shielded Twisted Pair Harness",
                "sku": "IR-CBL-485",
                "category": "Cables & Connectors",
                "moq": "50 Sets",
                "badge": None,
                "is_featured": False,
                "short_description": "Noise-immune industrial communication cable assembly for Modbus, CNC, and factory automation.",
                "specifications": {"Impedance": "120 Ohm", "Jacket": "Flame-Retardant PVC", "Length": "3m", "Contacts": "Gold-Plated Brass"},
                "color": (51, 65, 85),
            },
            {
                "title": "48V 15A Industrial Automation Power Controller",
                "sku": "IR-AUT-4815",
                "category": "Industrial Automation",
                "moq": "10 Units",
                "badge": Product.BadgeChoice.NEW_ARRIVAL,
                "is_featured": False,
                "short_description": "High-efficiency regulated DC supply tailored for stepper drivers, servo motors, and CNC rigs.",
                "specifications": {"Output": "48V DC / 15A (720W)", "Ripple": "< 150mVp-p", "Enclosure": "Vented Aluminum", "Warranty": "12 Months B2B"},
                "color": (127, 29, 29),
            },
            {
                "title": "Multi-Sensor Industrial Telemetry PCB Module",
                "sku": "IR-SNS-900",
                "category": "Sensors & Modules",
                "moq": "40 Pcs",
                "badge": Product.BadgeChoice.TRENDING,
                "is_featured": False,
                "short_description": "Pre-calibrated industrial temperature, humidity, and current-sensing daughterboard for IoT gateways.",
                "specifications": {"Protocol": "I2C / UART / RS485", "Supply": "5V / 3.3V Dual", "Accuracy": "+/- 0.3C", "Form Factor": "45x32mm PCB"},
                "color": (6, 78, 59),
            },
        ]

        for p_data in products_data:
            color = p_data["color"]
            cat_name = p_data["category"]
            defaults = {
                key: value
                for key, value in p_data.items()
                if key not in {"sku", "color", "category"}
            }
            defaults.update(
                {"category": cat_map[cat_name], "is_active": True}
            )
            product, _ = Product.objects.update_or_create(
                sku=p_data["sku"],
                defaults=defaults,
            )

            # 4. ProductImages
            existing_orders = set(
                product.images.values_list("sort_order", flat=True)
            )
            for idx in range(2):
                if idx in existing_orders:
                    continue
                p_img = ProductImage(
                    product=product,
                    alt_text=f"{product.title} - View {idx + 1}",
                    sort_order=idx,
                )
                p_img.image.save(
                    f"{product.slug}-{idx + 1}.png",
                    make_placeholder_image(f"{product.sku} (View {idx + 1})", color),
                    save=True,
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded IR Electronics sample data. Media files are in {settings.MEDIA_ROOT}."
            )
        )