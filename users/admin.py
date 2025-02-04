from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

class BaseUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'region')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'region')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_superuser'),
        }),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        (_('Personal info'), {'fields': ('email', 'region')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_superuser'),
        }),
    )
admin.site.register(User, BaseUserAdmin)

admin.site.register(Regions)