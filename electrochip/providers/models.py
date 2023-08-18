from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.text import slugify

from electrochip import validators as custom_validators

UserModel = get_user_model()


class Company(models.Model):
    MAX_NAME_LEN = 100
    MAX_CITY_NAME_LEN = 50
    MAX_COUNTRY_NAME_LEN = 30
    MIN_COUNTRY_NAME_LEN = 4
    MAX_ADDRESS_LEN = 200
    MIN_ADDRESS_LEN = 5
    MAX_PHONE_LEN = 20
    MAX_COMPANY_ID_LEN = 20
    MIN_COMPANY_ID_LEN = 8
    URL_MAX_LEN = 2083

    class Meta:
        verbose_name = 'Service Provider'
        verbose_name_plural = "Service Providers"

    name = models.CharField(
        max_length=MAX_NAME_LEN,
        null=False,
        blank=False,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
    )

    is_freelance = models.BooleanField(
        default=True,
    )

    company_logo = models.URLField(
        max_length=URL_MAX_LEN,
        blank=True,
        null=True
    )

    country = models.CharField(
        max_length=MAX_CITY_NAME_LEN,
        validators=[validators.MinLengthValidator(MIN_COUNTRY_NAME_LEN)],
        null=False,
        blank=False,
    )

    city = models.CharField(
        max_length=MAX_CITY_NAME_LEN,
        null=True,
        blank=True,
    )

    address = models.CharField(
        max_length=MAX_CITY_NAME_LEN,
        validators=[validators.MinLengthValidator(MIN_ADDRESS_LEN)],
        null=False,
        blank=False,
    )

    email = models.EmailField(
        blank=False,
        null=False,
        unique=True,
    )

    phone = models.CharField(
        max_length=15,
        validators=[custom_validators.validate_phone_number],
        blank=True,
        null=False,
    )

    company_national_id = models.CharField(
        max_length=MAX_COMPANY_ID_LEN,
        validators=[validators.MinLengthValidator(MIN_COMPANY_ID_LEN)],
        null=True,
        blank=True,
    )

    owner = models.ForeignKey(
        to=UserModel,
        on_delete=models.SET_NULL,
        related_name='owned_companies',  # Specify a custom related name
        null=True,  # Can be null if user is deleted, admin has to replace owner eventually
        blank=False,  # Cannot be empty upon creation
    )

    representatives = models.ManyToManyField(
        to=UserModel,
        related_name='representing_companies',  # Specify a custom related name
        blank=True
    )

    # services = models.ManyToManyField(
    #     to=Services,
    #     blank=True,
    #     related_name='company',
    # )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
