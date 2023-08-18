"""
URL configuration for electrochip project.
"""

from django.contrib import admin
from django.urls import path, include

from electrochip.exception_handlers import restricted_access_403, page_not_found_404, server_error_500
from electrochip.views import index, anchor_redirect, blog, about, contact, RestrictedAccessView

urlpatterns = [
    path('', index, name='index'),
    path('anchors/<str:section>/', anchor_redirect, name='anchor_redirect'),
    path('blog/', blog, name='blog'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('account/', include('electrochip.accounts.urls')),
    path('services/', include('electrochip.services.urls')),
    path('provider/', include('electrochip.providers.urls')),

    path('restricted-access/', RestrictedAccessView.as_view(), name='restricted_access'),

    path('admin/', admin.site.urls),
]

handler403 = restricted_access_403
handler404 = page_not_found_404
handler500 = server_error_500
