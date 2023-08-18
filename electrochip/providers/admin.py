from django.contrib import admin
from django.utils.html import format_html

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name_plural = "Companies"

    list_display = (
        'name',
        'picture_display',
        'is_freelance',
        'owner',
        'slug',
        'email',
        'phone',
        'country',
        'city',
        'address',
        'company_national_id',
    )
    list_filter = (
        'is_freelance',
        'city',
        'country',
    )
    search_fields = (
        'name',
        'slug',
        'country',
        'city',
        'email',
        'phone',
        'company_national_id',
        'owner__username',
        'owner__email',
    )
    readonly_fields = ('slug',)

    filter_horizontal = ('representatives',)

    @staticmethod
    def picture_display(obj):
        return format_html('<img src="{}" style="height:45px;" />'.format(obj.company_logo))
