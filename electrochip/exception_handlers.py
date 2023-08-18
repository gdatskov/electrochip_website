from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django.urls import reverse


def restricted_access_403(request, exception):
    context = {'status': 403}

    if isinstance(request.user, AnonymousUser):
        context['is_authenticated'] = False
    else:
        context['is_authenticated'] = True

    return render(request, 'restricted_access_403.html', context)


def page_not_found_404(request, exception):
    return render(request, 'page_not_found_404.html', status=404)


def server_error_500(request):
    return render(request, 'server_error_500.html', status=500)
