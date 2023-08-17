"""
URL configuration for electrochip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from electrochip.exception_handlers import restricted_access_403
from electrochip.settings import DEBUG
from electrochip.views import *

urlpatterns = [
    path('', index, name='index'),
    # TODO: service views
    path('anchors/<str:section>/', anchor_redirect, name='anchor_redirect'),
    path('blog/', blog, name='blog'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('account/', include('electrochip.accounts.urls')),
    path('service/', include('electrochip.services.urls')),
    path('provider/', include('electrochip.providers.urls')),

]
# TODO: Admin site - accessible only if logged user is staff (do not ask for login and redirect if not)
if DEBUG:
    urlpatterns.extend([
        path('admin/', admin.site.urls),
    ])

handler403 = restricted_access_403
