from .forms import SignupForm, EditProfileForm, EditFacultyDetailsForm, EditStudentDetailsForm, StudentRegistrationForm, FacultyRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views import View
import os


class UserLoginView(View):
    """ This view handles login requests, user authentication and validation. """
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {'LoginForm': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user_acc = authenticate(username=username, password=password)

            if user_acc is None:    # check if user account exists.
                messages.error(request, 'Invalid credentials! Please try again.')
                return redirect('login')
            
            else:
                if user_acc.is_student is True:
                    login(request, user_acc)
                    return redirect('student_homepage')   # redirect user to student's homepage
                
                else:
                    login(request, user_acc)
                    return redirect('faculty_homepage')   # redirect user to faculty's staff homepage

        context = {'LoginForm': form}
        return render(request, self.template_name, context)

def show_faculty_registration_form(wizard):
    """ 
        This function will be used to show the appropriate wizard form based on the user's selection.
        If the user selects radio button 'student', show StudentRegistrationForm.
        If the user selects radio button 'HOD/Lecturer', show FacultyRegistrationForm.
    """
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    is_student =  cleaned_data.get('is_student')
    return not is_student   # negate value; if "is_student" is True, return False and vice versa.

class SignupView(SessionWizardView):
    """ This view enables a user to create new account. """
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))
    form_list = [SignupForm, FacultyRegistrationForm, StudentRegistrationForm]
    template_name = 'accounts/signup.html'
    condition_dict = {
        '1': show_faculty_registration_form,  # Show FacultyRegistrationForm if is_student is False
        '2': lambda wizard: not show_faculty_registration_form(wizard)  # Show StudentRegistrationForm if is_student is True
    }

    def done(self, form_list, **kwargs):
        user_form = form_list[0]

        if user_form.cleaned_data.get('is_student') is True:
            user = user_form.save()
            new_student = form_list[1].save(commit=False)
            new_student.student_name = user
            new_student.save()

        else:
            user = user_form.save()
            new_faculty_staff = form_list[1].save(commit=False)
            new_faculty_staff.staff = user
            new_faculty_staff.save()

        messages.success(self.request, 'Account successfully created!')
        return redirect('login')

@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False or user.is_superuser is False), name='get')
class EditStudentProfileView(View):
    profile_form_class = EditProfileForm
    student_form_class = EditStudentDetailsForm
    template_name = 'dashboard/students/profile.html'

    def get(self, request, _student_name, *args, **kwargs):
        editprofile_form = self.profile_form_class(instance=request.user)
        editstudent_form = self.student_form_class(instance=request.user.student)

        context = {
            'EditProfileForm': editprofile_form,
            'UpdateStudentInfoForm': editstudent_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, _student_name, *args, **kwargs):
        editprofile_form = self.profile_form_class(request.POST, request.FILES, instance=request.user)
        editstudent_form = self.student_form_class(request.POST, instance=request.user.student)

        if editprofile_form.is_valid():
            editprofile_form.save()

            messages.info(request, 'User profile updated successfully')
            return redirect('student_profile', _student_name)
        
        elif editstudent_form.is_valid():
            editstudent_form.save()

            messages.info(request, 'Student details updated successfully')
            return redirect('student_profile', _student_name)

        context = {
            'EditProfileForm': editprofile_form,
            'UpdateStudentInfoForm': editstudent_form,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False or user.is_superuser is False), name='get')
class EditFacultyStaffProfileView(View):
    profile_form_class = EditProfileForm
    faculty_form_class = EditFacultyDetailsForm
    template_name = 'dashboard/faculty/profile.html'

    def get(self, request, staff_name, *args, **kwargs):
        editprofile_form = self.profile_form_class(instance=request.user)
        editfaculty_form = self.faculty_form_class(instance=request.user.faculty)

        context = {
            'EditProfileForm': editprofile_form,
            'UpdateFacultyDetailsForm': editfaculty_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, staff_name, *args, **kwargs):
        editprofile_form = self.profile_form_class(request.POST, request.FILES, instance=request.user)
        editfaculty_form = self.faculty_form_class(request.POST, instance=request.user.faculty)

        if editprofile_form.is_valid():
            editprofile_form.save()

            messages.info(request, 'User profile updated successfully')
            return redirect('faculty_profile', staff_name)
        
        elif editfaculty_form.is_valid():
            editfaculty_form.save()

            messages.info(request, 'Staff details updated successfully')
            return redirect('faculty_profile', staff_name)

        context = {
            'EditProfileForm': editprofile_form,
            'UpdateFacultyDetailsForm': editfaculty_form,
        }
        return render(request, self.template_name, context)


class LogoutUserView(LogoutView):
    template_name = 'accounts/login.html'
