from django.shortcuts import render
from django.shortcuts import render_to_response, redirect, resolve_url
from django.views.generic import TemplateView

from apps.accounts.choices import RoleUser


def error400(request, exception):
    response = render_to_response('errors/error_400.html', {})
    response.status_code = 400
    return response


def error403(request, exception):
    response = render_to_response('errors/error_403.html', {})
    response.status_code = 403
    return response


def error404(request, exception):
    response = render_to_response('errors/error_404.html', {})
    response.status_code = 404
    return response


def error500(request):
    response = render_to_response('errors/error_500.html', {})
    response.status_code = 500
    return response


class Home(TemplateView):
    template_name = 'base.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.role in [RoleUser.Expert, RoleUser.Administrator]:
                return redirect('contests:contests')
            elif user.role == RoleUser.User:
                return redirect('contests:final_results')
        else:
            return redirect('contests:final_results')