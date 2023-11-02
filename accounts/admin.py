from .models import Faculty, Student, User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User
from .forms import SignupForm

class UserLayout(UserAdmin):
    model = User
    add_form = SignupForm
    list_display = ['username', 'email', 'gender', 'is_student', 'date_joined']
    readonly_fields = ['last_login', 'date_joined']

    fieldsets = (
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username', 'email', 'gender', 'dob', 'mobile_no', 'is_student')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, UserLayout)

@admin.register(Student)
class StudentsDetailsTable(admin.ModelAdmin):
    list_display = ['student_name', 'school', 'programme', 'year', 'semester']
    readonly_fields = ['student_name', 'school', 'programme', 'year', 'semester']

@admin.register(Faculty)
class FacultyRecords(admin.ModelAdmin):
    list_display = ['staff', 'department', 'position']
    readonly_fields = ['staff', 'department', 'position']
