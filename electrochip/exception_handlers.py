from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django.urls import reverse


def restricted_access_403(request, exception):
    context = {}

    if isinstance(request.user, AnonymousUser):
        context['is_authenticated'] = False
    else:
        context['is_authenticated'] = True

    return render(request, 'restricted_access.html', context)
