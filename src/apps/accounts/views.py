from django.shortcuts import redirect, get_object_or_404, render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth
from django.contrib.auth import logout as auth_logout
from django.views.generic import UpdateView
from django.views.generic.edit import FormView, View
from django.urls import reverse_lazy

from apps.accounts.forms import LoginForm, UpdateForm
from apps.accounts.choices import RoleUser


class LoginUserView(FormView):
    """ Авторизация """
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()
        auth.login(self.request, user)
        if user.role in [RoleUser.Expert, RoleUser.Administrator]:
            return redirect('contests:contests')
        return redirect('contests:final_results')
        # return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class LogoutFormView(View):
    """ Выход из профиля """
    def get(self, request):
        auth_logout(request)
        return redirect('contests:final_results')


class UpdateUserView(UpdateView):
    """ Детальная информация об авторизованном пользователе с возможностью редактирования """
    template_name = 'accounts/data_user.html'
    form_class = UpdateForm
    success_url = reverse_lazy('accounts:my_data')

    def get_object(self, queryset=None):
        return self.request.user
