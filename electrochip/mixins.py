from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy


class RestrictedAccessMixin(UserPassesTestMixin):
    login_url = reverse_lazy('restricted_access')  # Redirect to the restricted_access page
    raise_exception = True  # Raise a PermissionDenied exception

    def test_func(self):
        return self.login_url
