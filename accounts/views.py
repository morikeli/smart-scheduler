from .forms import SignupForm, EditProfileForm, StudentRegistrationForm, FacultyRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.conf import settings
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
class EditProfileView(View):
    form_class = EditProfileForm
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)

        context = {'EditProfileForm': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()

            messages.info(request, 'User profile updated successfully')
            return redirect('profile')

        context = {'EditProfileForm': form}
        return render(request, self.template_name, context)


class LogoutUser(LogoutView):
    template_name = 'accounts/logout.html'
