from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile

# Register your models here.

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (StudentProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile)
