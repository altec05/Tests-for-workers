from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('username', 'last_name', 'first_name', 'patronymic', 'year_of_birth', 'job', 'department', 'email',
                    'is_staff', 'is_active', 'created_at')
    list_display_links = ('username',)
    search_fields = ('username', 'last_name', 'job')
    list_filter = ('job', 'department', 'is_staff', 'is_active')
    readonly_fields = ('created_at',)
    fields = ('username', 'last_name', 'first_name', 'patronymic', 'year_of_birth', 'job', 'department', 'email',
              'is_staff', 'is_active', 'created_at', 'groups', 'user_permissions')


admin.site.register(User, UserAdmin)
