from django.contrib import admin
from .models import User,CustomerProfile,DriverProfile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display= ('email','is_superuser','is_active','is_verified')
    list_filter = ('email','is_superuser','is_active','is_verified','is_driver','is_customer')
    search_fields=('email',)
    ordering = ('email',)
    fieldsets = (
        ('Authentications', {
            "fields": (
                'email','password'
            ),
        }),
        ('permissions',
        {
            "fields":(
                'is_staff','is_active','is_superuser','is_verified','is_driver','is_customer',
            )
        }),
        ('group permissions',
        {
            "fields":(
                'groups','user_permissions'
            )
        }),
        ('date',
        {
            "fields":(
               'last_login',
            )
        }),
         ('Token',
        {
            "fields":(
               'Token',
            )
        }),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2","is_staff",'is_active','is_superuser','is_verified','is_customer','is_driver'),
            },
        ),
    )

admin.site.register(User,CustomUserAdmin)
admin.site.register(CustomerProfile)
admin.site.register(DriverProfile)