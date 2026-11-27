from django.db import migrations, models


def remove_redundant_media_prefix(apps, schema_editor):
    database = schema_editor.connection.alias
    fields_by_model = {
        "Category": ("image",),
        "CompanyConfig": ("logo", "favicon", "hero_background_image"),
    }

    for model_name, field_names in fields_by_model.items():
        model = apps.get_model("shop", model_name)
        for field_name in field_names:
            queryset = model.objects.using(database).filter(
                **{f"{field_name}__startswith": "media/"}
            )
            for instance in queryset.iterator():
                value = getattr(instance, field_name).name
                setattr(instance, field_name, value[len("media/"):])
                instance.save(using=database, update_fields=[field_name])


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_alter_category_slug_alter_product_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="cateogry/"
            ),
        ),
        migrations.AlterField(
            model_name="companyconfig",
            name="logo",
            field=models.ImageField(upload_to="assets/"),
        ),
        migrations.AlterField(
            model_name="companyconfig",
            name="favicon",
            field=models.ImageField(upload_to="assets/"),
        ),
        migrations.AlterField(
            model_name="companyconfig",
            name="hero_background_image",
            field=models.ImageField(upload_to="assets/"),
        ),
        migrations.RunPython(
            remove_redundant_media_prefix, migrations.RunPython.noop
        ),
    ]
