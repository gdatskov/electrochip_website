from django.urls import path, include

from electrochip.accounts.views import *
# from electrochip.services.views import BecomeProvider

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', include([
        # path('<int:pk>/', UserProfileView.as_view(), name='profile'),
        path('edit/', EditUserProfileView.as_view(), name='edit_profile'),
        path('<slug:slug>/', UserProfileView.as_view(), name='profile'),
    ])),
    path('restricted-access/', RestrictedAccessView.as_view(), name='restricted_access'),
]
