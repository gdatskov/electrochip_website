from django.shortcuts import render, redirect
from django.urls import reverse
from electrochip.services import models as app_models
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

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


def user_detail_view(request, pk):
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, pk=pk)
    return render(request, 'admin/user_detail.html', {'user': user})
