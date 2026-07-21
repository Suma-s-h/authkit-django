from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('bio', 'location', 'birth_date', 'gender', 'phone', 'website', 'avatar_color')


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'phone', 'gender', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('user__username', 'user__email', 'location', 'phone')
    readonly_fields = ('created_at', 'updated_at')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.site_header = 'AuthKit Administration'
admin.site.site_title = 'AuthKit Admin'
admin.site.index_title = 'Welcome to AuthKit Admin Panel'
