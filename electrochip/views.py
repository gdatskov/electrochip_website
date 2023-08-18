from django.contrib.admin import site as admin_site
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from electrochip.services import models as app_models
from django.db.models import Sum
from django.shortcuts import render


def staff_check(user):
    return user.is_authenticated and user.is_staff


def custom_admin_login(request, **kwargs):
    if staff_check(request.user):
        return admin_site.login(request, **kwargs)
    else:
        return redirect(reverse('index'))  # Redirect non-staff users to the home page

def index(request):
    categories = app_models.ServicesCategory.objects.annotate(
        popularity_sum=Sum('services__popularity')
    ).exclude(is_default=True) \
                     .order_by('-popularity_sum', 'id')[:3]

    context = {'category_list': categories}

    return render(request, 'index.html', context)


def about(request):
    return render(request, 'extensions/about.html')


def about_anchor(request):
    return redirect(reverse('index') + '#about')


def services_anchor(request):
    return redirect(reverse('index') + '#services')


def blog(request):
    return render(request, 'extensions/blog.html')


def blog_anchor(request):
    return redirect(reverse('index') + '#blog')


def contact(request):
    return render(request, 'extensions/contact.html', context={})


def contact_anchor(request):
    return redirect(reverse('index') + '#contact')


def anchor_redirect(request, section):
    if section in ['services', 'about', 'blog', 'contact']:
        return redirect(reverse('index') + f'#{section}')
    else:
        # Handle invalid section parameter
        return redirect(reverse('index'))


class RestrictedAccessView(TemplateView):
    template_name = 'restricted_access_403.html'
