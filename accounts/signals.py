from django.db.models.signals import pre_save
from django import dispatch
from datetime import datetime
from uuid import uuid4
from .models import User, Faculty, Student

@dispatch.receiver(pre_save, sender=User)
def generate_userID(sender, instance, *args, **kwargs):
    if instance.id == '':
        instance.id = str(uuid4()).replace('-', '')[:25]

    try:
        if not instance.is_superuser is True:
            if datetime.now().strftime('%Y-%m-%d %H:%M:%S') > instance.date_joined.strftime('%Y-%m-%d %H:%M:%S'):
                user_dob = str(instance.dob)
                get_user_dob = datetime.strptime(user_dob, '%Y-%m-%d')
                current_date = datetime.now()
                user_age = current_date - get_user_dob
                convert_user_age = int(user_age.days/365.25)
                instance.age = convert_user_age
                
            else:
                user_dob = str(instance.dob)
                get_user_dob = datetime.strptime(user_dob, '%Y-%m-%d')
                current_date = datetime.now()
                user_age = current_date - get_user_dob
                convert_user_age = int(user_age.days/365.25)
                instance.age = convert_user_age
    
    except AttributeError:
        return
    
@dispatch.receiver(pre_save, sender=Faculty)
def generate_facultyID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid4()).replace('-', '')[:30]

@dispatch.receiver(pre_save, sender=Student)
def generate_studentID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid4()).replace('-', '')[:30]
