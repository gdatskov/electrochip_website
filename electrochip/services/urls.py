from django.urls import path, include
from electrochip.services.views import *

urlpatterns = [
        path('', AllCategoriesListView.as_view(), name='service categories'),
        path('category/', category_services_list_view, name='service category'),
        path('<int:pk>/', ServiceDetailsView.as_view(), name='service_details'),
        path('<int:pk>/edit', EditServiceView.as_view(), name='edit_service'),
        path('all/', all_services_list_view, name='all_services_list'),    # TODO: check if needed
        path('add/', AddServiceView.as_view(), name='add_service'),
]
