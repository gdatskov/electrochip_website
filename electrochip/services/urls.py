from django.urls import path, include
from electrochip.services.views import *

urlpatterns = [
        path('', AllCategoriesList.as_view(), name='service categories'),
        # path('category/<int:pk>/', category_services_list, name='service category'),
        path('category/', category_services_list, name='service category'),
        path('<int:pk>/', ServiceDetails.as_view(), name='service_details'),
        path('all/', all_services_list, name='all_services_list'),    # TODO: check if needed
        path('add/', AddService.as_view(), name='add_service'),
]
