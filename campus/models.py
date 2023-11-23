from accounts.models import Student, Faculty
from django.db import models

class BookedUnit(models.Model):
    """ These are records of units assigned to a lecturer each semester. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    lecturer = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    students_course = models.CharField(max_length=50, blank=False)
    course_name = models.CharField(max_length=80, blank=False)
    year_of_study = models.CharField(max_length=10, blank=False)
    semester = models.CharField(max_length=1, blank=False)
    booking_date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.course_name
    
    class Meta:
        ordering = ['course_name', 'lecturer']
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
        ordering = ['unit', 'student']
        verbose_name_plural = 'Registered units'
    
    def __str__(self) -> str:
        return self.student

class Lecture(models.Model):
    """ This db table stores records of all scheduled lectures. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    lecturer = models.ForeignKey(Faculty, on_delete=models.CASCADE, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, editable=False)
    lecture_hall = models.ForeignKey('LectureHall', on_delete=models.CASCADE, editable=False, null=True, db_column='Venue')
    unit_name = models.ForeignKey(BookedUnit, on_delete=models.CASCADE)
    lecture_date = models.DateField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False, db_column='Scheduled start time')    # lecture should start at this time
    end_time = models.TimeField(null=False, blank=False, db_column='Scheduled end time')     # lecture should end at this time
    recurrence_pattern = models.CharField(max_length=10, blank=False)
    total_students = models.PositiveIntegerField(default=0, editable=False)     # approximate no. of students expected to attend the lecture.
    is_attending = models.BooleanField(default=False)   # is the student attending the lecture?
    is_taught = models.BooleanField(default=False, editable=False)  # was the class taught or it "bounced".
    date_scheduled = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['lecturer', 'lecture_hall', '-date_scheduled']
        verbose_name_plural = 'Scheduled lectures'

class Notification(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    message = models.CharField(max_length=100)
    scheduled_lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.scheduled_lecture.unit_name}'
    
    class Meta:
        ordering = ['-date_created', 'message']
        verbose_name_plural = 'Notifications'

class LectureHall(models.Model):
    """ This db table stores records of all available lecture halls in the entire institution. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    academic_block = models.CharField(max_length=20, blank=False)
    hall_no = models.CharField(max_length=5, unique=True, blank=False)
    seating_capacity = models.PositiveIntegerField(default=0)
    floor = models.CharField(max_length=7, blank=False)
    rating = models.PositiveIntegerField(default=0, editable=False)
    image = models.ImageField(upload_to='Lecture-Halls/img/', default='lecture-hall.jpg')
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
    complaint = models.CharField(max_length=30, blank=False)
    description = models.TextField()
    rate_score = models.PositiveIntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.lecture_hall}'
    
    class Meta:
        ordering = ['lecture_hall', '-date_posted']
        verbose_name_plural = 'Feedback'
