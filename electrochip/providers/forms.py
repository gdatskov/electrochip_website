from django import forms

from electrochip.providers.models import Company


class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'country', 'city', 'address', 'company_national_id', 'email', 'phone']


class FreelanceRegistrationForm(AddCompanyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide not needed fields
        self.fields['name'].widget = forms.HiddenInput()
        self.fields['company_national_id'].widget = forms.HiddenInput()
