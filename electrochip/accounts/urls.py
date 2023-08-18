from django.urls import path, include

from electrochip.accounts.views import *
# from electrochip.services.views import BecomeProvider

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', include([
        path('edit/', EditUserProfileView.as_view(), name='edit_profile'),
        path('<slug:slug>/', UserProfileView.as_view(), name='profile'),
    ])),
]
