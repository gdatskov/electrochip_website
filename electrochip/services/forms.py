from django import forms

from electrochip.services.models import Services


class AddServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name', 'short_description', 'picture', 'category']

