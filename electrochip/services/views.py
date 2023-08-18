from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic as generic_views

from electrochip.mixins import RestrictedAccessMixin
from electrochip.providers.models import Company
from electrochip.services.forms import AddServiceForm
from electrochip.services import models as app_models

UserModel = get_user_model()


class AddServiceView(LoginRequiredMixin, RestrictedAccessMixin, generic_views.CreateView):
    model = app_models.Services
    template_name = 'services/add_service_form.html'
    form_class = AddServiceForm

    def form_valid(self, form):
        owner = self.request.user

        # Set the owner (logged-in user) as the owner of the new service
        form.instance.owner = owner

        # Get the associated company for the logged-in user
        company = Company.objects.get(owner=owner)
        form.instance.company = company

        return super().form_valid(form)

    def get_success_url(self):
        provider = get_object_or_404(Company, owner_id=self.request.user.pk)
        return reverse('provider_services', kwargs={'slug': provider.slug})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Exclude the default category from the category choices. It should be used for admin stuff only.
        form.fields['category'].queryset = app_models.ServicesCategory.objects.exclude(is_default=True)
        return form


class AllCategoriesListView(generic_views.ListView):
    model = app_models.ServicesCategory
    template_name = 'extensions/service_categories.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        return app_models.ServicesCategory.objects.exclude(is_default=True)


def paginate_services(request, services):
    paginator = Paginator(services, per_page=5)
    page_number = request.GET.get('page')

    try:
        page_services = paginator.page(page_number)
    except PageNotAnInteger:
        page_services = paginator.page(1)
    except EmptyPage:
        page_services = paginator.page(paginator.num_pages)

    return page_services


def all_services_list_view(request):
    query = request.GET.get('q')
    services = app_models.Services.objects.select_related('category', 'owner').all()

    if query:
        services = services.filter(name__icontains=query)

    page_services = paginate_services(request, services)

    context = {
        'page_services': page_services,
        'query': query,
    }

    return render(request, 'services/all_services_list.html', context)


def category_services_list_view(request):
    all_categories = app_models.ServicesCategory.objects.all()
    selected_category = request.GET.get('category')
    query = request.GET.get('q')

    category = None
    services = app_models.Services.objects.all()

    if selected_category:
        category = get_object_or_404(app_models.ServicesCategory, pk=selected_category)
        services = services.filter(category=category)

    if query:
        services = services.filter(name__icontains=query)

    for index, service in enumerate(services, start=1):
        service.row_number = index

    page_services = paginate_services(request, services)

    selected_category_pk = int(selected_category) if selected_category else None
    selected_category_name = category.name if category else 'All'
    context = {
        'page_services': page_services,
        'all_categories': all_categories,
        'selected_category_pk': selected_category_pk,
        'selected_category_name': selected_category_name,
        'query': query,
    }

    return render(request, 'services/category_services_list.html', context)


class ServiceDetailsView(LoginRequiredMixin, RestrictedAccessMixin, generic_views.DetailView):
    model = app_models.Services
    template_name = 'services/service_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        service = self.object
        owner = service.owner
        provider = Company.objects.get(owner=owner)

        additional_descriptions = service.serviceadditionaldescription_set.values_list('description', flat=True)

        context['provider'] = provider
        context['additional_descriptions'] = additional_descriptions
        context['is_owner'] = self.object.owner == self.request.user

        return context


class EditServiceView(ServiceDetailsView, generic_views.UpdateView):
    template_name = 'services/add_service_form.html'
    fields = ['name', 'short_description', 'picture', 'category']

    def dispatch(self, request, *args, **kwargs):
        # Get the service object
        self.object = self.get_object()

        # Check if the logged-in user is the owner of the service
        if self.object.owner != self.request.user:
            return redirect('restricted_access')  # Redirect to 'restricted_access' view

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('service_details', kwargs={'pk': self.object.pk})
