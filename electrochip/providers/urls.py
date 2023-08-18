from django.urls import path, include
from electrochip.providers.views import *

urlpatterns = [
    path('<slug:slug>/', include([
        path('', ProviderProfileView.as_view(), name='provider_details'),
        path('services/', provider_services_list_view, name='provider_services'),
    ])),
    # path('all/', ProviderServiceList.as_view(), name='all providers'),    # TODO: Change view name
    # path('add/', BecomeProvider.as_view(), name='add provider'),  # TODO: Is it needed?
    path('register/', include([
        path('freelance/', FreelanceRegistrationView.as_view(), name='freelance_registration'),
        path('company/', CompanyRegistrationView.as_view(), name='company_registration'),
    ]))
]
