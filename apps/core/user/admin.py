from django.contrib import admin
from apps.core.user.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.db import models


class UserAdminConfig(UserAdmin):
    model = User
    ordering = ('-start_date',)
    search_fields = (
        'email',
        'username',
        'first_name',
        'auth_type'
    )
    list_filter = (
        'email',
        'username',
        'first_name',
        'is_active',
        'is_staff',
        'auth_type'
    )
    list_display = (
        'email',
        'username',
        'first_name',
        'is_active',
        'is_staff',
        'auth_type'
    )
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'username',
                'first_name',
                'auth_type',
                'uuid',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_staff',
                'is_active',
            )
        }),
    )
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 20, 'cols': 60}),
        }
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'first_name',
                'password1',
                'password2',
                'is_active',
                'is_staff',
            )
        }),
    )


admin.site.register(User, UserAdminConfig)
