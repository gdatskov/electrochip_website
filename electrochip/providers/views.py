from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic as generic_views

from electrochip.mixins import RestrictedAccessMixin
from electrochip.providers.forms import FreelanceRegistrationForm, AddCompanyForm
from electrochip.providers import models as provider_app_models
from electrochip.services import models as service_app_models

UserModel = get_user_model()


# TODO: Check if needed
# class BecomeProvider(LoginRequiredMixin, RestrictedAccessMixin,  generic_views.View):
#     template_name = 'services/freelancer_registration_form.html'
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {'freelance_registration_form': FreelanceRegistrationForm()})
#
#     def post(self, request, *args, **kwargs):
#         registration_type = request.POST.get('registration_type')
#         if registration_type == 'freelance':
#             return redirect('freelance_registration')
#         elif registration_type == 'company':
#             return redirect('company_registration')


class FreelanceRegistrationView(LoginRequiredMixin, RestrictedAccessMixin, generic_views.CreateView):
    model = provider_app_models.Company
    template_name = 'services/freelancer_registration_form.html'
    form_class = FreelanceRegistrationForm

    def form_valid(self, form):
        # Set the owner (logged-in user) as the owner of the new company (freelancer)
        # TODO test if can register without logged in user
        form.instance.owner = self.request.user

        # Set is_freelancer to True for freelancer registration
        form.instance.is_freelancer = True

        # Set is_provider to True for the logged-in user
        self.request.user.is_provider = True
        self.request.user.save()

        return super().form_valid(form)

    def get_initial(self):
        # Set the initial value for the 'name' field using the user's full name
        full_name = self.request.user.get_full_name()
        return {'name': full_name}

    def get_success_url(self):
        provider_slug = self.object.slug
        return reverse('provider_details', kwargs={'slug': provider_slug})


class CompanyRegistrationView(LoginRequiredMixin, RestrictedAccessMixin, generic_views.CreateView):
    model = provider_app_models.Company
    template_name = 'services/provider_registration_form.html'
    form_class = AddCompanyForm

    def form_valid(self, form):
        # Set the owner (logged-in user) as the owner of the new company
        form.instance.owner = self.request.user

        # Set is_freelancer to False for company registration
        form.instance.is_freelance = False

        # Set is_provider to True for the logged-in user
        self.request.user.is_provider = True

        self.request.user.save()

        return super().form_valid(form)

    def get_success_url(self):
        # TODO: fix redirect
        # Redirect to the "AddService" form after company registration
        return reverse('provider details', kwargs={
            'pk': self.object.pk})  # Replace 'add service' with your URL name for the "AddService" form


def provider_services_list(request, slug):

    provider = get_object_or_404(provider_app_models.Company, slug=slug)
    owner = provider.owner
    services = service_app_models.Services.objects.filter(owner=owner)
    category = service_app_models.ServicesCategory.objects.filter(services__in=services).distinct()

    # page_services = paginate_services(request, services)

    context = {
        'provider': provider,
        'category': category,
        # 'page_services': page_services,
    }

    return render(request, 'services/provider_services_list.html', context)


class ProviderServices(generic_views.ListView):
    model = service_app_models.ServicesCategory
    template_name = 'services/provider_services_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        provider = provider_app_models.Company.objects.get(pk=self.kwargs['pk'])

        # Get all services associated with the provider's company
        provider_services = provider.services.all()

        context['provider'] = provider
        context['provider_services'] = provider_services

        return context


class ProviderProfile(LoginRequiredMixin, RestrictedAccessMixin, generic_views.DetailView):
    model = provider_app_models.Company
    template_name = 'services/service_provider_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.object

        # Get the provider's services (associated with the company)
        provider_services = service_app_models.Services.objects.filter(owner_id=company.id)

        context['company'] = company
        context['provider_services'] = provider_services
        context['is_owner'] = company.owner_id == self.request.user.id

        return context

    def get_object(self):
        provider_slug = self.kwargs.get('slug')
        return get_object_or_404(self.model, slug=provider_slug)


