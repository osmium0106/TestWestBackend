from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserPreference

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Limits', {
            'fields': ('role', 'max_sub_users', 'max_question_papers', 'parent')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & Limits', {
            'fields': ('role', 'max_sub_users', 'max_question_papers', 'parent')
        }),
    )
    list_display = ('username', 'email', 'role', 'max_sub_users', 'parent', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')

admin.site.register(UserPreference)
