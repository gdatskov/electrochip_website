# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from django.apps import apps
# from django.core.exceptions import ObjectDoesNotExist
# from django.utils import timezone
#
# from .models import ServicesCategory
#
#
# @receiver(post_migrate)
# def create_standard_categories(sender, **kwargs):
#     default_description = 'There are many variations of passages of Lorem Ipsum available,'
#
#     # Check if the migration '0002_create_default_category' has been applied for the 'services' app
#     if sender.name == 'services' and '0002_create_default_category' in kwargs['plan']:
#
#         # Migration 0002_create_default_category has been applied, so add the standard categories
#         category_data = [
#             {
#                 'name': "Equipment installation",
#                 'description': default_description,
#                 'picture': 'images/s1.png',
#                 'is_default': False,
#                 'date_added': timezone.now(),
#                 'date_modified': timezone.now(),
#                 'is_new_category': False,
#             },
#             {
#                 'name': "Windmill Energy",
#                 'description': default_description,
#                 'picture': 'images/s2.png',
#                 'is_default': False,
#                 'date_added': timezone.now(),
#                 'date_modified': timezone.now(),
#                 'is_new_category': False,
#             },
#             {
#                 'name': "Equipment Maintenance",
#                 'description': default_description,
#                 'picture': 'images/s3.png',
#                 'is_default': False,
#                 'date_added': timezone.now(),
#                 'date_modified': timezone.now(),
#                 'is_new_category': False,
#             },
#             {
#                 'name': "Offshore Engineering",
#                 'description': default_description,
#                 'picture': 'images/s4.png',
#                 'is_default': False,
#                 'date_added': timezone.now(),
#                 'date_modified': timezone.now(),
#                 'is_new_category': False,
#             },
#             {
#                 'name': "Electrical Wiring",
#                 'description': default_description,
#                 'picture': 'images/s5.png',
#                 'is_default': False,
#                 'date_added': timezone.now(),
#                 'date_modified': timezone.now(),
#                 'is_new_category': False,
#             },
#         ]
#
#         for category_info in category_data:
#             category_name = category_info['name']
#             if not ServicesCategory.objects.filter(name=category_name).exists():
#                 category = ServicesCategory(**category_info)
#                 category.save()

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from django.utils import timezone

from .models import ServicesCategory


# TODO: Check Signals if needed
@receiver(post_migrate)
def create_standard_categories(sender, **kwargs):
    default_description = 'There are many variations of passages of Lorem Ipsum available,'

    # Check if the migration '0002_create_default_category' has been applied for the 'services' app
    if sender.name == 'services' and '0002_create_default_category' in kwargs['plan']:
        print("Migration '0002_create_default_category' has been applied.")
        # Migration 0002_create_default_category has been applied, so add the standard categories
        category_data = [
            # ...
            # your category data
        ]

        for category_info in category_data:
            category_name = category_info['name']
            if not ServicesCategory.objects.filter(name=category_name).exists():
                print(f"Creating category: {category_name}")
                category = ServicesCategory(**category_info)
                category.save()
        print("Standard categories created.")
    else:
        print("Migration '0002_create_default_category' has not been applied.")
