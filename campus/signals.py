from .models import BookedUnit, Faculty, Feedback, Lecture, LectureHall, RegisteredUnit, School, Student
from django.db.models.signals import pre_save
from django import dispatch
import uuid


@dispatch.receiver(pre_save, sender=BookedUnit)
def generate_booked_unitID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4()).replace('-', '')[:30]

@dispatch.receiver(pre_save, sender=Faculty)
def generate_facultyID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4()).replace('-', '')[:30]

@dispatch.receiver(pre_save, sender=Feedback)
def generate_feedbackID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4()).replace('-', '')[:30]

@dispatch.receiver(pre_save, sender=Lecture)
def generate_lectureID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4()).replace('-', '')[:30]

@dispatch.receiver(pre_save, sender=LectureHall)
def generate_lecture_hallID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4()).replace('-', '')[:30]

@dispatch.receiver(pre_save, sender=RegisteredUnit)
def generate_registered_unitID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4()).replace('-', '')[:30]

@dispatch.receiver(pre_save, sender=School)
def generate_schoolID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4()).replace('-', '')[:30]

@dispatch.receiver(pre_save, sender=Student)
def generate_studentID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4()).replace('-', '')[:30]
