from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic as generic_views

from electrochip.services.forms import AddServiceForm
from electrochip.services import models as app_models

UserModel = get_user_model()


# TODO: Test all login required views

class AddService(generic_views.CreateView):
    model = app_models.Services
    template_name = 'services/add_service_form.html'
    form_class = AddServiceForm

    def form_valid(self, form):
        # TODO Set the owner (logged-in user) as the owner of the new service
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to a success page after adding the service
        return reverse('all services')  # TODO Replace 'service_added' with the appropriate URL name

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Exclude the default category from the category choices. It should be used for admin stuff only.
        form.fields['category'].queryset = app_models.ServicesCategory.objects.exclude(is_default=True)
        return form


class AllCategoriesList(generic_views.ListView):
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


def all_services_list(request):
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


def category_services_list(request):
    all_categories = app_models.ServicesCategory.objects.all()
    selected_category = request.GET.get('category')
    query = request.GET.get('q')

    services = app_models.Services.objects.all()

    if selected_category:
        category = get_object_or_404(app_models.ServicesCategory, pk=selected_category)
        services = services.filter(category=category)

    if query:
        services = services.filter(name__icontains=query)

    page_services = paginate_services(request, services)

    context = {
        'page_services': page_services,
        'all_categories': all_categories,
        'selected_category': int(selected_category) if selected_category else None,
        'query': query,
    }

    return render(request, 'services/category_services_list.html', context)


class ServiceDetails(generic_views.DetailView):
    model = app_models.Services
    template_name = 'services/service_details.html'


