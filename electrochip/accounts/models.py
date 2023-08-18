from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class AppUser(AbstractUser):
    USERNAME_MAX_LEN = 30
    FIRST_NAME_MAX_LEN = 30
    LAST_NAME_MAX_LEN = 30
    URL_MAX_LEN = 2083
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=USERNAME_MAX_LEN,
        unique=True,
        blank=False,
        null=False,
        help_text=_(
            f"Required. {USERNAME_MAX_LEN} characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    slug = models.SlugField(
        unique=True,
    )

    first_name = models.CharField(
        _("first name"),
        max_length=FIRST_NAME_MAX_LEN,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        _("last name"),
        max_length=LAST_NAME_MAX_LEN,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        _("email address"),
        blank=False,
        null=False,
        unique=True,
    )

    is_provider = models.BooleanField(
        _("provider status"),
        default=False,
        help_text=_("Designates whether the user is provider."),
    )

    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
    )

    profile_picture = models.URLField(
        max_length=URL_MAX_LEN,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
