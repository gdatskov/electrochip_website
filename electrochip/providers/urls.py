from django.urls import path, include
from electrochip.providers.views import *

urlpatterns = [
    path('<int:pk>/', include([
        path('', ProviderProfile.as_view(), name='provider details'),
        path('services/', provider_services_list, name='provider services'),
    ])),
    # path('all/', ProviderServiceList.as_view(), name='all providers'),    # TODO: Change view name
    path('add/', BecomeProvider.as_view(), name='add provider'),  # TODO check add
    path('register/', include([
        path('freelance/', FreelanceRegistrationView.as_view(), name='freelance_registration'),
        path('company/', CompanyRegistrationView.as_view(), name='company_registration'),
    ]))
]
