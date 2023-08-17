from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views, login, logout, get_user_model  # LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views import generic as generic_views  # CreateView, DetailView, UpdateView
from django.views.generic import UpdateView, DetailView, TemplateView

from electrochip.accounts import forms
from electrochip.accounts.forms import RegisterUserForm, EditUserProfileForm
from electrochip.accounts.mixins import RestrictedAccessMixin
from electrochip.accounts.models import AppUser

UserModel = get_user_model()


class Login(auth_views.LoginView):
    template_name = 'account/login.html'
    # fields = ('username', 'password')
    next_page = reverse_lazy('index')


class Register(generic_views.CreateView):
    template_name = 'account/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    # Automatically login after registration
    def form_valid(self, form):
        # Call the custom clean_username method to perform validation
        try:
            form.clean_username()
        except forms.ValidationError as e:
            # If the username validation fails, re-render the form with the error message
            return self.form_invalid(form)

        # If the username validation passes, proceed with normal registration process
        response = super().form_valid(form)

        # Generate slug for the user
        self.object.save()

        # Automatically login after registration
        login(self.request, self.object)

        return response


@login_required
def logout_view(request):
    if request.method == 'GET':
        return render(request, 'account/logout.html')
    elif request.method == 'POST':
        # Perform the logout and redirect
        logout(request)
        return redirect('index')  # Redirect to the index page


def get_full_name(user):
    first_name = user.first_name if user.first_name is not None else ''
    last_name = user.last_name if user.last_name is not None else ''
    full_name = f"{first_name} {last_name}".strip()
    return full_name


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'account/user_profile.html'

    def get_queryset(self):
        # Get user by slug instead of pk
        return UserModel.objects.filter(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['full_name'] = get_full_name(self.object)
        context['is_owner'] = self.object == self.request.user
        return context

    def generate_slug(self):
        slug = slugify(self.object.name)
        return slug  # Use the slugified username as the slug


class EditUserProfileView(LoginRequiredMixin, UpdateView):
    model = UserModel  # Specify the model for the view
    form_class = EditUserProfileForm    # Use the EditUserProfileForm
    template_name = 'account/edit_user_profile.html'  # Specify the template for the view

    #
    # def get_queryset(self):
    #     return UserModel.objects

    def get_object(self):
        # Return the currently logged-in user's profile
        # print()
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Set default values for optional fields
        optional_fields = ['first_name', 'last_name', 'profile_picture']
        for field_name in optional_fields:
            if not getattr(form.instance, field_name):
                setattr(form.instance, field_name, 'default value')

        return form

    def get_success_url(self):
        return reverse('profile')




class RestrictedAccessView(TemplateView):
    template_name = 'account/../../templates/restricted_access.html'
