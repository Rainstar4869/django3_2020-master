from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from mptt.admin import MPTTModelAdmin
from .models import User, Profile


class AccountAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_superuser', 'introcode', 'parent_introcode')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('username', 'avatar')}),
        ('Localization', {'fields': ('language', 'timezone')}),
        ('Introcode info', {'fields': ('introcode', 'parent_introcode')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password1', 'password2')}),
        ('Personal info', {'fields': ('username', 'avatar')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email', 'name')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, AccountAdmin)
admin.site.register(
    Profile,
    MPTTModelAdmin,
)
