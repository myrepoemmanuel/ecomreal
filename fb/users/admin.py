
from django.contrib import admin
from django.forms import Textarea
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.admin import UserAdmin

# Register your models here.

User = get_user_model()
class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'user_name', 'full_name',)
    list_filter = ('email', 'user_name', 'full_name', 'is_active', 'is_staff')
    ordering = ('-date_join',)
    list_display = ('email', 'user_name', 'full_name', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'full_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
        ('Personal', {'fields': ('about',)})
        
    )

    formfield_overrides = {
        User.about: {'widget': Textarea(attrs={'rows':20, 'cols': 40})}
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name','full_name', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )

admin.site.register(User, UserAdminConfig)
admin.site.register(Profile)