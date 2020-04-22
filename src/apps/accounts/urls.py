# -*- coding:utf-8 -*-
from django.urls import path

from apps.accounts.views import LoginUserView, LogoutFormView, UpdateUserView
from apps.accounts.decorators import login_required

app_name = 'accounts'

urlpatterns = [
    path('my_data/', login_required(UpdateUserView.as_view()), name='my_data'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutFormView.as_view(), name='logout'),
]
