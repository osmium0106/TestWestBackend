from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserPreference

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Limits', {
            'fields': ('role', 'max_sub_users', 'max_question_papers', 'parent',
                       'school_name', 'school_address', 'school_contact_number',
                       'school_director_name', 'school_billing_email', 'max_question_school_can_generate')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & Limits', {
            'fields': ('role', 'max_sub_users', 'max_question_papers', 'parent',
                       'school_name', 'school_address', 'school_contact_number',
                       'school_director_name', 'school_billing_email', 'max_question_school_can_generate')
        }),
    )
    list_display = ('username', 'email', 'role', 'max_sub_users', 'parent', 'school_name', 'school_contact_number', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'school_name')

admin.site.register(UserPreference)
