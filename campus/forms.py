from .models import BookedUnit, Feedback, Lecture, LectureHall, RegisteredUnit
from accounts.models import School
from django import forms

class SchoolRegistrationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-0',
        }),
        help_text='Enter the name of the school',
        label='School',
    )

    class Meta:
        model = School
        fields = ['name']

class AddLectureHallForm(forms.ModelForm):
    SELECT_FLOOR = (
        (None, '-- Select floor --'),
        ('GF', 'Ground floor'),
        ('1', 'First floor'),
        ('2', 'Second floor'),
        ('3', 'Third floor'),
        ('4', 'Fourth floor'),
    )

    academic_block = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-0',
        }),
        help_text='On which academic block is lecture hall located?',
        label='Academic block',    
    )
    hall_no = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-0',
        }),
        help_text='Enter the hall number or name of the hall/room',
        label='Lecture room/hall no.',
    )
    floor = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-0',
        }),
        choices=SELECT_FLOOR,
        help_text='Enter floor number of the hall',
        label='Floor',    
    )

    class Meta:
        model = LectureHall
        fields = ['academic_block', 'hall_no', 'floor']

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

class LecturerUnitsBookingForm(forms.ModelForm):
    SELECT_YEAR_OF_STUDY = (
        (None, '-- Select year of study --'),
        ('1', 'First years (Freshers)'),
        ('2', 'Second years (Sophomores)'),
        ('3', 'Third years (Juniors)'),
        ('4', 'Fourth years (Seniors)'),
    )
    SELECT_SEMESTER = (
        (None, '-- Select course name --'),
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
    )
    
    lecturer = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
    )
    course_name = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
    )
    
    year_of_study = forms.ChoiceField(widget=forms.Select(attrs={
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
        model = BookedUnit
        fields = ['lecturer', 'course_name', 'year_of_study', 'semester']

class LectureSchedulingForm(forms.ModelForm):
    SELECT_RECURRENCE_PATTERN = (
        (None, '-- Select one choice'),
        ('Once', 'Once'),
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
    )

    unit_name = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        label='Unit',
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
        fields = ['unit_name', 'lecture_date', 'start_time', 'end_time', 'recurrence_pattern']

class FeedbackForm(forms.ModelForm):
    SELECT_TYPE_COMPLAINT = (
        (None, '-- Select type of complaint --'),
        ('Burnt bulbs', 'Burnt bulbs/flourescent tubes'),
        ('Dirty whiteboard', 'Dirty whiteboard (Permanent marker used)'),
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
            'type': 'text', 'class': 'mb-0', 'placeholder': 'Provide more details about your complaints/approvals ...',
        }),
        help_text='What are your complaints or what you love about this lecture hall/room.',   
    )
    rate = forms.CharField(widget=forms.NumberInput(attrs={
            'type': 'number', 'class': 'mb-0', 'min': 0, 'max': 5,
        }),
        help_text='How do you rate this hall?',
        label='Rating',    
    )

    class Meta:
        model = Feedback
        fields = ['complaint', 'description', 'rate']
