from django.db import migrations
from django.utils import timezone


def create_default_categories(apps, schema_editor):
    ServicesCategory = apps.get_model('services', 'ServicesCategory')

    default_description = 'There are many variations of passages of Lorem Ipsum available,'

    default_categories = [
                    {
                        'name': "Equipment installation",
                        'description': default_description,
                        'picture': 'images/s1.png',
                        'is_new_category': False,
                    },
                    {
                        'name': "Windmill Energy",
                        'description': default_description,
                        'picture': 'images/s2.png',
                        'is_new_category': False,
                    },
                    {
                        'name': "Equipment Maintenance",
                        'description': default_description,
                        'picture': 'images/s3.png',
                        'is_new_category': False,
                    },
                    {
                        'name': "Offshore Engineering",
                        'description': default_description,
                        'picture': 'images/s4.png',
                        'is_new_category': False,
                    },
                    {
                        'name': "Electrical Wiring",
                        'description': default_description,
                        'picture': 'images/s5.png',
                        'is_new_category': False,
                    },
    ]

    for category_info in default_categories:
        category_name = category_info['name']
        if not ServicesCategory.objects.filter(name=category_name).exists():
            category = ServicesCategory(**category_info)
            category.save()


class Migration(migrations.Migration):
    dependencies = [
        ('services', '0002_create_default_category'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]
