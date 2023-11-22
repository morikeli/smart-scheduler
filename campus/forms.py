from .models import BookedUnit, Feedback, Lecture, RegisteredUnit
from accounts.models import Faculty
from django import forms

class StudentUnitsRegistrationForm(forms.ModelForm):
    unit = forms.ChoiceField(widget=forms.SelectMultiple(attrs={
            'type': 'select', 'class': 'mb-0',
        }),
        help_text='You can select multiple units.',
        label='Units',    
    )

    class Meta:
        model = RegisteredUnit
        fields = ['unit']

class StudentsAttendanceConfirmationForm(forms.ModelForm):
    lecture_date = forms.DateField(widget=forms.DateInput(attrs={
            'type': 'date', 'class': 'mb-0',
        }),
        help_text='Schedule a date for this lecture',
        disabled=True,
    )
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={
            'type': 'time', 'class': 'mb-0',
        }),
        help_text='At what time will this lecture begin?',
        label='Schedule start time',
        disabled=True,
    )
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={
            'type': 'time', 'class': 'mb-0',
        }),
        help_text='At what time will this lecture end?',
        label='Schedule end time',
        disabled=True,
    )
    is_attending = forms.BooleanField(widget=forms.CheckboxInput(attrs={
            'type': 'checkbox', 'class': 'my-2',
        }),
        help_text='I will be attending the class',
        required=True,
    )

    class Meta:
        model = Lecture
        fields = ['lecture_date', 'start_time', 'end_time', 'is_attending']

class LecturerUnitsBookingForm(forms.ModelForm):
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
        ('1st year', 'First years (Freshers)'),
        ('2nd year', 'Second years (Sophomores)'),
        ('3rd year', 'Third years (Juniors)'),
        ('4th year', 'Fourth years (Seniors)'),
    )
    SELECT_SEMESTER = (
        (None, '-- Select semester --'),
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
    )
    
    course_name = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'select', 'class': 'mb-0',
        }),
        label='Unit name',
        help_text='Enter the name of the unit (<b>Enter course code & course title</b>)<br>'
    )
    students_course = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-0',
        }),
        choices=SELECT_STUDENT_COURSE,
        label='Students course group',
        help_text='Which students will be studying this unit?'
    )
    year_of_study = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-0',
        }),
        choices=SELECT_YEAR_OF_STUDY,
        label='Year of study',
        help_text='This unit will be studied by students of which year?',
    )
    semester = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-0',
        }),
        choices=SELECT_SEMESTER,
        help_text='This unit will be studied by students of which semester?',
    )

    def __init__(self, *args, **kwargs):
        super(LecturerUnitsBookingForm, self).__init__(*args, **kwargs)
        # Filter all faculty staff in the OneToOneField dropdown
        self.fields['lecturer'].queryset = Faculty.objects.filter()

    class Meta:
        model = BookedUnit
        fields = ['lecturer', 'course_name', 'students_course',  'year_of_study', 'semester']

class FeedbackForm(forms.ModelForm):
    SELECT_TYPE_COMPLAINT = (
        (None, '-- Select type of complaint --'),
        ('Burnt bulbs', 'Burnt bulbs/flourescent tubes'),
        ('Dirty whiteboard', 'Dirty whiteboard (Permanent marker used)'),
        ('Dysfunctional ethernet port', 'Dysfunctional ethernet ports'),
        ('Dysfunctional sockets', 'Dysfunctional sockets'),
        ('Environmental noise', 'Environmental noise'),
        ('Naked electrical wires', 'Naked electrical wires'),
        ('No seats', 'No seats'),
        ('Poor lighting', 'Poor lighting'),
        ('Unfavorable temperature', 'Unfavorable temperature i.e. too cold/hot'),
    )

    complaint = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-0',
        }),
        choices=SELECT_TYPE_COMPLAINT,
        label='Complaints', 
    )
    description = forms.CharField(widget=forms.Textarea(attrs={
            'type': 'text', 'class': 'mb-0', 'placeholder': 'Provide more details about your complaints/approvals about this room/hall ...',
        }),
        help_text='What are your complaints or what you love about this lecture hall/room.',   
    )
    rate_score = forms.CharField(widget=forms.NumberInput(attrs={
            'type': 'number', 'class': 'mb-0', 'min': 0, 'max': 5,
        }),
        help_text='How do you rate this hall?',
        label='Rating',    
    )

    class Meta:
        model = Feedback
        fields = ['complaint', 'description', 'rate_score']


# Edit forms

class EditScheduledLectureForm(forms.ModelForm):
    SELECT_RECURRENCE_PATTERN = (
        (None, '-- Select one choice --'),
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    )

    lecture_date = forms.DateField(widget=forms.DateInput(attrs={
            'type': 'date', 'class': 'mb-0',
        }),
        help_text='Schedule a date for this lecture',    
    )
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={
            'type': 'time', 'class': 'mb-0',
        }),
        help_text='At what time will this lecture begin?',
        label='Schedule start time',
    )
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={
            'type': 'time', 'class': 'mb-0',
        }),
        help_text='At what time will this lecture end?',
        label='Schedule end time',
    )
    recurrence_pattern = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'text', 'class': 'mb-0',
        }),
        help_text='Schedule lecture once, daily or weekly',
        label='Recurrence mode',
        choices=SELECT_RECURRENCE_PATTERN,
    )

    class Meta:
        model = Lecture
        fields = ['lecture_date', 'start_time', 'end_time', 'recurrence_pattern']
