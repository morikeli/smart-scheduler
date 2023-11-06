from django.contrib.auth.forms import UserCreationForm
from .utils import validate_image_file
from .models import Student, Faculty
from django import forms
from .models import User

SELECT_SCHOOL = (
        (None, '-- Select your school --'),
        ('School of Arts, Social Sciences and Business', 'School of Arts, Social Sciences and Business (SASSB)'),
        ('School of Education', 'School of Education (SE)'),
        ('School of Information, Communication & Media Studies', 'School of Information, Communication & Media Studies (INFOCOMS)'),
        ('School of Science, Agriculture & Environmental Science', 'School of Science, Agriculture & Environmental Science (SSAES)'),
)

class SignupForm(UserCreationForm):
    SELECT_TYPE_USER = [
        (True, 'Student'),
        (False, 'HOD/Lecturer'),
    ]
    SELECT_GENDER = (
        (None, '-- Select your gender --'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-2', 'autofocus': True
        }),
        required=True,
    )
    last_name = forms.CharField(widget=forms.TextInput(attrs={
           'type': 'text', 'class': 'mb-2',
        }),
        required=True,
    )
    username = forms.CharField(widget=forms.TextInput(attrs={
           'type': 'text', 'class': 'mb-2',
        }),
        required=True,
    )
    mobile_no = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'tel', 'class': 'mb-0',
        }),
        help_text='Enter your phone number and include your country code, e.g. +254112345678'
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'type': 'email', 'class': 'mb-2',
        }),
    )
    gender = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=SELECT_GENDER,
    )
    dob = forms.DateField(widget=forms.DateInput(attrs={
            'type': 'date', 'class': 'mb-2',
        }),
        required=True,
    )
    is_student = forms.BooleanField(widget=forms.RadioSelect(attrs={
            'type': 'radio', 'class': 'mt-3 mb-0',
        },
        choices=SELECT_TYPE_USER
        ),
        required=False,
        label='Are you a student or lecturer/HOD?',
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile_no', 'gender', 'dob', 'is_student', 'password1', 'password2']

class StudentRegistrationForm(forms.ModelForm):
    SELECT_COURSE_PROGRAMME = (
        (None, '-- Select your course programme --'),
        ('Certificate', 'Certificate'),
        ('Degree', "Bachelor's Degree"),
        ('Diploma', 'Diploma'),
    )
    SELECT_STUDENT_COURSE = (
        (None, '-- Select your course --'),
        ('Agribusiness', 'Agricultural Business'),
        ('Applied mathematics', 'Applied Mathematics'),
        ('Applied statictics', 'Applied Statictics'),
        ('Computer Science', 'Computer Science'),
        ('Education', 'Education'),
    )
    SELECT_YEAR_OF_STUDY = (
        (None, '-- Select year of study --'),
        ('1st year', 'First year (Freshers)'),
        ('2nd year', 'Second year (Sophomores)'),
        ('3rd year', 'Third year (Juniors)'),
        ('4th year', 'Fourth year (Seniors)'),
    )
    SELECT_SEMESTER = (
        (None, '-- Select semester --'),
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
    )

    school = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        label='School',
        choices=SELECT_SCHOOL,
    )
    reg_no = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-2',
        }),
        label='Registration Number',
    )
    programme = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=SELECT_COURSE_PROGRAMME,
        label='Course programme',    
    )
    course = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=SELECT_STUDENT_COURSE,
        label='Course name',    
    )
    year = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=SELECT_YEAR_OF_STUDY,
        label='Year of study',    
    )
    semester = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=SELECT_SEMESTER,    
    )

    class Meta:
        model = Student
        fields = ['school', 'reg_no', 'year', 'semester', 'programme']

class FacultyRegistrationForm(forms.ModelForm):
    SELECT_FACULTY_ROLE = (
        (None, '-- Select one choice --'),
        ('HOD', 'Head of Department (HOD)'),
        ('Lecturer', 'Lecturer'),
    )
    
    school = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        label='School',
        choices=SELECT_SCHOOL,
    )
    department = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-2',
        }),
    )
    position = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        label='Role',
        choices=SELECT_FACULTY_ROLE,
    )

    class Meta:
        model = Faculty
        fields = ['school', 'department', 'position']

# Edit forms

class EditProfileForm(forms.ModelForm):
    SELECT_GENDER = (
        (None, '-- Select your gender --'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    SELECT_COUNTRY = (
        (None, '-- Select your country of origin --'),
        ('Kenya', 'Kenya'),
    )

    first_name = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-2', 'autofocus': True
        }),
        required=True,
        disabled=True,
    )
    last_name = forms.CharField(widget=forms.TextInput(attrs={
           'type': 'text', 'class': 'mb-2',
        }),
        required=True,
        disabled=True,
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'type': 'email', 'class': 'mb-2',
        }),
    )
    gender = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=SELECT_GENDER,
        disabled=True,
    )
    dob = forms.DateField(widget=forms.DateInput(attrs={
            'type': 'date', 'class': 'mb-2',
        }),
        required=True,
        disabled=True,
    )
    mobile_no = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'tel', 'class': 'mb-0',
        }),
        help_text='Enter your phone number and include your country code, e.g. +254112345678'
    )
    profile_pic = forms.FileField(
        widget=forms.FileInput(attrs={
            'type': 'file', 'class': 'form-control mb-2', 'accept': '.jpg, .jpeg, .png',
        }),
        required=False,
        validators=[validate_image_file],
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'dob', 'mobile_no', 'profile_pic']

class EditStudentDetailsForm(forms.ModelForm):
    SELECT_COURSE_PROGRAMME = (
        (None, '-- Select your course programme --'),
        ('Certificate', 'Certificate'),
        ('Degree', "Bachelor's Degree"),
        ('Diploma', 'Diploma'),
    )
    SELECT_YEAR_OF_STUDY = (
        (None, '-- Select year of study --'),
        ('1st year', 'First year (Fresher)'),
        ('2nd year', 'Second year (Sophomore)'),
        ('3rd year', 'Third year (Junior)'),
        ('4th year', 'Fourth year (Senior)'),
    )
    SELECT_SEMESTER = (
        (None, '-- Select semester --'),
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
    )

    school = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        label='School',
        choices=SELECT_SCHOOL,
        disabled=True,
    )
    reg_no = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-2',
        }),
        label='Registration Number',
        disabled=True,
    )
    programme = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=SELECT_COURSE_PROGRAMME,
        label='Course programme',
        disabled=True,
    )
    year = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=SELECT_YEAR_OF_STUDY,
        label='Year of study',    
    )
    semester = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=SELECT_SEMESTER,    
    )

    class Meta:
        model = Student
        fields = ['programme', 'school', 'reg_no', 'year', 'semester']

class EditFacultyDetailsForm(forms.ModelForm):
    SELECT_FACULTY_ROLE = (
        (None, '-- Select one choice --'),
        ('HOD', 'Head of Department (HOD)'),
        ('Lecturer', 'Lecturer'),
    )
    
    school = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        label='School',
        choices=SELECT_SCHOOL,
        disabled=True,
    )
    department = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-2',
        }),
        disabled=True,
    )
    position = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        label='Role',
        choices=SELECT_FACULTY_ROLE,
        disabled=True,
    )

    class Meta:
        model = Faculty
        fields = ['school', 'department', 'position']
