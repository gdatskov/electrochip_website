from django.db import migrations


def create_default_category(apps, schema_editor):
    ServicesCategory = apps.get_model('services', 'ServicesCategory')

    default_category_name = 'No category'
    default_category_picture_path = 'images/no-category.png'

    default_category = ServicesCategory(
        name=default_category_name,
        picture=default_category_picture_path,
        is_default=True,
        is_new_category=False,
    )

    default_category.save()


class Migration(migrations.Migration):
    dependencies = [
        ('services', '0001_services_category'),
    ]

    operations = [
        migrations.RunPython(create_default_category),
    ]