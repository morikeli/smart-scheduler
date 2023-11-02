from accounts.models import User
from django.db import models


class School(models.Model):
    """ This model stores records of all schools in the campus. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=70, blank=False)     # name of the school.
    total_students = models.PositiveIntegerField(default=0, editable=False)
    total_staff = models.PositiveIntegerField(default=0, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'School records'

    def __str__(self) -> str:
        return self.name

class Student(models.Model):
    """ This model stores info about students records. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    student_name = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=14, blank=False, unique=True, db_column='Registration No.')
    year = models.CharField(max_length=10, blank=False, db_column='Year of Study')
    semester = models.CharField(max_length=1, blank=False)
    programme = models.CharField(max_length=35, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_name', 'reg_no']
        verbose_name_plural = 'Students records'
    
    def __str__(self) -> str or None:
        return self.student_name
    
class Faculty(models.Model):
    """ This db table stores records of all staff in a given faculty. In this case lecturer and HOD are the only members in the faculty. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    staff = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    department = models.CharField(max_length=40, blank=False)
    position = models.CharField(max_length=20, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.staff
    
    class Meta:
        ordering = ['staff', 'school']
        verbose_name_plural = 'Faculty records'

class BookedUnit(models.Model):
    """ These are records of units assigned to a lecturer each semester. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    lecturer = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=80, blank=False)
    year_of_study = models.CharField(max_length=10, blank=False)
    semester = models.CharField(max_length=1, blank=False)
    booking_date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.course_name
    
    class Meta:
        ordering = ['lecturer', 'course_name']
        verbose_name_plural = 'Booked units'

class RegisteredUnit(models.Model):
    """ These are records for units a student has registered in a given semester. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, editable=False)
    unit = models.ForeignKey(BookedUnit, on_delete=models.CASCADE)
    is_registered = models.BooleanField(default=False, editable=False)
    date_registered = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student', 'unit']
        verbose_name_plural = 'Registered units'
    
    def __str__(self) -> str:
        return self.student

class Lecture(models.Model):
    """ This db table stores records of all scheduled lectures. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    lecturer = models.ForeignKey(Faculty, on_delete=models.CASCADE, editable=False)
    lecture_hall = models.ForeignKey('LectureHall', on_delete=models.CASCADE, editable=False)
    unit_name = models.ForeignKey(BookedUnit, on_delete=models.CASCADE)
    lecture_date = models.DateField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False, db_column='Scheduled start time')    # lecture should start at this time
    end_time = models.TimeField(null=False, blank=False, db_column='Scheduled end time')     # lecture should end at this time
    recurrence_pattern = models.CharField(max_length=10, blank=False)
    total_students = models.PositiveIntegerField(default=0, editable=False)     # approximate no. of students expected to attend the lecture.
    is_taught = models.BooleanField(default=False, editable=False)  # was the class taught or it "bounced".
    date_scheduled = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['lecturer', 'lecture_hall', '-date_scheduled']
        verbose_name_plural = 'Scheduled lectures'

class LectureHall(models.Model):
    """ This db table stores records of all available lecture halls in the entire institution. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    academic_block = models.CharField(max_length=20, blank=False)
    hall_no = models.CharField(max_length=5, blank=False)
    seating_capacity = models.PositiveIntegerField(default=0, editable=False)
    floor = models.CharField(max_length=7, blank=False)
    rating = models.PositiveIntegerField(default=0, editable=False)
    image = models.ImageField(upload_to='Lecture-Halls/img/', default='lecture-hall.png')
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.hall_no
    
    class Meta:
        ordering = ['academic_block', 'hall_no']
        verbose_name_plural = 'Lecture halls'

class Feedback(models.Model):
    """ These are records of students feedback about lecture halls assigned for a given lecture. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, editable=False)
    lecture_hall = models.ForeignKey(LectureHall, on_delete=models.CASCADE, editable=False)
    complaint = models.CharField(max_length=20, blank=False)
    description = models.TextField()
    rate_score = models.PositiveIntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.lecture_hall
    
    class Meta:
        ordering = ['lecture_hall', '-date_posted']
        verbose_name_plural = 'Feedback'
