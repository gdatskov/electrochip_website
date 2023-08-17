from django.urls import path, include
from electrochip.services.views import *

urlpatterns = [
        path('', AllCategoriesList.as_view(), name='service categories'),
        # path('category/<int:pk>/', category_services_list, name='service category'),
        path('category/', category_services_list, name='service category'),
        path('<int:pk>/', ServiceDetails.as_view(), name='service details'),
        path('all/', all_services_list, name='all_services_list'),    # TODO check all
        path('add/', AddService.as_view(), name='add service'),
]
