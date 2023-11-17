from .models import BookedUnit, Feedback, Lecture, LectureHall, Notification, RegisteredUnit
from django.db.models.signals import pre_save, post_save
from .utils import schedule_recurring_lectures
from django import dispatch
import schedule
import uuid


@dispatch.receiver(pre_save, sender=BookedUnit)
def generate_booked_unitID(sender, instance, **kwargs):
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

@dispatch.receiver(pre_save, sender=Notification)
def generate_notificationsID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4()).replace('-', '')[:30]

@dispatch.receiver(post_save, sender=Lecture)
def save_lecture_record(sender, instance, created, **kwargs):
    if created:
        # Schedule the class when a new class is created
        if instance.recurrence_pattern == 'once': pass
        else:
            schedule_recurring_lectures()   # check if instance is a recurring lecture. If True, call schedule_recurring_lectures()
