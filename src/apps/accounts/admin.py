# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.accounts.models import User
from apps.accounts.forms import UserChangeForm, UserCreationForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('phone_number', 'email', 'last_name', 'first_name',)
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    readonly_fields = ('password',)
    search_fields = ('last_name', 'first_name', 'middle_name')
    save_on_top = True
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password',)}),
        ('Персональная информация', {'fields': ('last_name', 'first_name', 'middle_name', 'role',
                                                'password1', 'password2')}),
        ('Права доступа', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', )}),
        ('Важные даты', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'last_name', 'first_name', 'middle_name', 'subdivision', 'phone_number')}
         ),
    )
