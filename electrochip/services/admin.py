from django.contrib import admin
from django.utils.html import format_html

from .forms import AddServiceForm
from .models import Services, ServicesCategory, ServiceAdditionalDescription, ServicePhotos


@admin.register(ServicesCategory)
class ServicesCategoryAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = "Service categories"

    list_display = (
        'name',
        'description',
        'picture_display',
        'date_added',
        'date_modified',
        'is_default',
        'is_new_category',
    )
    list_filter = ('is_new_category',)
    search_fields = (
        'name',
        'description'
    )
    readonly_fields = (
        'date_added',
        'date_modified'
    )
    ordering = (
        '-is_new_category',
        'is_default',
        '-date_modified',
        '-date_added',
    )

    @staticmethod
    def picture_display(obj):
        return format_html('<img src="{}" style="height:45px;" />'.format(obj.picture))


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    add_form = AddServiceForm

    class Meta:
        verbose_name_plural = "Services"

    list_display = (
        'name',
        'category',
        'short_description',
        'picture_display',
        'owner',
        'popularity',
        'date_added',
        'date_modified',
    )
    list_filter = (
        'popularity',
        'date_added',
        'category'
        )
    search_fields = (
        'name',
        'short_description'
    )
    readonly_fields = (
        'popularity',
        'date_added',
        'date_modified'
    )

    @staticmethod
    def picture_display(obj):
        return format_html('<img src="{}" style="height:45px;" />'.format(obj.picture))


@admin.register(ServiceAdditionalDescription)
class ServiceAdditionalDescriptionAdmin(admin.ModelAdmin):
    list_display = ('description', 'service')
    search_fields = ('description', 'service__name')


@admin.register(ServicePhotos)
class ServicePhotosAdmin(admin.ModelAdmin):
    list_display = ('picture_display', 'description', 'service_association', 'description_association')
    search_fields = ('photo', 'description', 'service_association__name', 'description_association__description')

    @staticmethod
    def picture_display(obj):
        return format_html('<img src="{}" style="height:45px;" />'.format(obj.photo))