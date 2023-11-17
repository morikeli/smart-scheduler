from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    first_name = models.CharField(max_length=15, blank=False)
    last_name = models.CharField(max_length=15, blank=False)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=7, blank=False)
    dob = models.DateField(null=True, blank=False, db_column='Date of Birth')
    age = models.PositiveIntegerField(default=0, editable=False)
    mobile_no = PhoneNumberField()
    profile_pic = models.ImageField(upload_to='Users/imgs/dps/', default='default.png')
    is_student = models.BooleanField(default=False)
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username
    
    class Meta:
        ordering = ['username', 'first_name', 'last_name']

class Student(models.Model):
    """ This model stores info about students records. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    student_name = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    school = models.CharField(max_length=70, blank=False)
    department = models.CharField(max_length=70, blank=False)
    reg_no = models.CharField(max_length=14, blank=False, unique=True, db_column='Registration No.')
    year = models.CharField(max_length=10, blank=False, db_column='Year of Study')
    semester = models.CharField(max_length=1, blank=False)
    programme = models.CharField(max_length=35, blank=False)
    course = models.CharField(max_length=50, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_name', 'reg_no']
        verbose_name_plural = 'Students records'
    
    def __str__(self) -> str:
        return f'{self.student_name}'

class Faculty(models.Model):
    """ This db table stores records of all staff in a given faculty. In this case lecturer and HOD are the only members in the faculty. """
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    staff = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    school = models.CharField(max_length=70, blank=False)
    department = models.CharField(max_length=40, blank=False)
    position = models.CharField(max_length=20, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.staff}'
    
    class Meta:
        ordering = ['staff', 'school']
        verbose_name_plural = 'Faculty records'
