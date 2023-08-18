from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from electrochip.providers.models import Company

UserModel = get_user_model()


class ServicesCategory(models.Model):
    MAX_NAME_LEN = 30
    MAX_DESCRIPTION_LEN = 200

    class Meta:
        verbose_name_plural = "Services Category"

    name = models.CharField(
        max_length=MAX_NAME_LEN,
        null=False,
        blank=False,
        unique=True,
    )

    description = models.TextField(
        max_length=MAX_DESCRIPTION_LEN,
        null=False,
        blank=False,
    )

    picture = models.URLField(
        blank=False,
        null=False
    )

    # Flag to mark the default category
    is_default = models.BooleanField(
        default=False,
        editable=False
    )

    date_added = models.DateTimeField(
        auto_now_add=timezone.now()
    )

    date_modified = models.DateTimeField(
        auto_now=timezone.now()
    )

    # New categories that have to be approved by staff
    is_new_category = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if this is the first category being created (is_default will only be set once)
        if not self.pk and not ServicesCategory.objects.filter(is_default=True).exists():
            self.is_default = True  # Mark this category as default
        super(ServicesCategory, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Check if this is the default category
        if self.is_default:
            raise ValidationError("The default category cannot be deleted.")
        super().delete(*args, **kwargs)


def get_default_category():
    default_category = ServicesCategory.objects.filter(is_default=True).first()
    if default_category:
        return default_category
    # If the default category doesn't exist, return a default value
    return None  # You can adjust this to another fallback value if needed


class Services(models.Model):
    MAX_NAME_LEN = 100
    MAX_DESCRIPTION_LEN = 200

    class Meta:
        verbose_name_plural = "Services"

    name = models.CharField(
        max_length=MAX_NAME_LEN,
        null=False,
        blank=False,
    )

    short_description = models.TextField(
        max_length=MAX_DESCRIPTION_LEN,
        null=False,
        blank=False,
    )

    picture = models.URLField(
        blank=True,
        null=True,
    )

    popularity = models.PositiveIntegerField(default=0)

    date_added = models.DateTimeField(
        auto_now_add=timezone.now()
    )

    date_modified = models.DateTimeField(
        auto_now=timezone.now()
    )

    category = models.ForeignKey(
        to=ServicesCategory,
        on_delete=models.SET_DEFAULT,
        default=get_default_category,
        related_name='services'
    )
    """
    Note:
    Mitigation of the problem that the default category might not be created during migration
    is ensured by first migrating ServicesCategory and creating the default category beforehand
    """

    owner = models.ForeignKey(
        to=UserModel,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name


class ServiceAdditionalDescription(models.Model):
    MAX_DESCRIPTION_LEN = 100

    class Meta:
        verbose_name_plural = "Services Additional Description"

    description = models.TextField(
        max_length=MAX_DESCRIPTION_LEN,
        null=False,
        blank=False,
    )

    service = models.ForeignKey(
        to=Services,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.description


class ServicePhotosManager(models.Manager):

    def create_photo(self, photo, description, service=None, description_association=None):
        if service is None and description_association is None:
            raise ValueError(
                "A photo must be associated with either a Service or a Service description."
            )

        create_photo = self.create(
            photo=photo,
            description=description,
            service_association=service,
            description_association=description_association
        )

        return create_photo


class ServicePhotos(models.Model):
    MAX_DESCRIPTION_LEN = 100

    class Meta:
        verbose_name_plural = "Services Photos"

    photo = models.URLField(
        blank=False,
        null=False,
    )

    description = models.TextField(
        max_length=MAX_DESCRIPTION_LEN,
        null=True,
        blank=True,
    )

    # Fields to associate the photo with Service and/or ServiceDescription
    service_association = models.ForeignKey(
        to='Services',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    description_association = models.ForeignKey(
        to=ServiceAdditionalDescription,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    objects = ServicePhotosManager()

    def delete(self, *args, **kwargs):
        # Ensure the photo is deleted only if the associated service is deleted
        if self.service_association is None:
            super().delete(*args, **kwargs)

    def __str__(self):
        return self.description
