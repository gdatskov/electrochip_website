from django.shortcuts import redirect
from django.urls import reverse


class RedirectNonStaffToHomePageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_url = reverse('admin:login')
        access_denied = not (request.user.is_staff or request.user.is_superuser)

        if request.path == admin_url and access_denied:
            return redirect(reverse('restricted_access'))

        return self.get_response(request)
