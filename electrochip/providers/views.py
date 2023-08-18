from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic as generic_views

from electrochip.mixins import RestrictedAccessMixin
from electrochip.providers.forms import FreelanceRegistrationForm, AddCompanyForm
from electrochip.providers import models as provider_app_models
from electrochip.services import models as service_app_models
from electrochip.services.views import paginate_services

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
    template_name = 'providers/freelancer_registration_form.html'
    form_class = FreelanceRegistrationForm

    def form_valid(self, form):
        # Set the owner (logged-in user) as the owner of the new company (freelancer)
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
    template_name = 'providers/provider_registration_form.html'
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
        return reverse('provider details', kwargs={
            'pk': self.object.pk})


# TODO: Merge functionality with category_services_list_view() since they have pretty much the same functionality
def provider_services_list_view(request, slug):
    provider = get_object_or_404(provider_app_models.Company, slug=slug)
    owner = provider.owner
    services = service_app_models.Services.objects.filter(owner=owner)
    category = service_app_models.ServicesCategory.objects.filter(services__in=services).distinct()

    all_categories = service_app_models.ServicesCategory.objects.all()
    selected_category = request.GET.get('category')
    query = request.GET.get('q')

    if selected_category:
        category = get_object_or_404(service_app_models.ServicesCategory, pk=selected_category)
        services = services.filter(category=category)
        selected_category_name = category.name
        selected_category_pk = int(selected_category)
    else:
        selected_category_name = "All categories"
        selected_category_pk = None

    if query:
        services = services.filter(name__icontains=query)

    for index, service in enumerate(services, start=1):
        service.row_number = index

    page_services = paginate_services(request, services)

    context = {
        'page_services': page_services,
        'all_categories': all_categories,
        'selected_category_pk': selected_category_pk,
        'selected_category_name': selected_category_name,
        'query': query,
        'provider': provider,
        'category': category,
    }

    return render(request, 'providers/provider_services_list.html', context)


class ProviderServicesView(generic_views.ListView):
    model = service_app_models.ServicesCategory
    template_name = 'providers/provider_services_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        provider = provider_app_models.Company.objects.get(pk=self.kwargs['pk'])

        # Get all services associated with the provider's company
        provider_services = provider.services.all()

        context['provider'] = provider
        context['provider_services'] = provider_services

        return context


class ProviderProfileView(LoginRequiredMixin, RestrictedAccessMixin, generic_views.DetailView):
    model = provider_app_models.Company
    template_name = 'providers/service_provider_profile.html'

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


class EditProviderProfileView(LoginRequiredMixin, RestrictedAccessMixin, generic_views.UpdateView):
    model = provider_app_models.Company
    template_name = 'providers/edit_provider_profile.html'

    fields = [
        'name',
        'name',
        'is_freelance',
        'company_logo',
        'city',
        'address',
        'phone',
        'company_national_id',
        'representatives',
    ]

    def dispatch(self, request, *args, **kwargs):
        # Get the provider object
        self.object = self.get_object()

        # Check if the logged-in user is the owner of the service
        if self.object.owner != self.request.user:
            return redirect('restricted_access')  # Redirect to 'restricted_access' view

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('provider_details', kwargs={'slug': self.object.slug})