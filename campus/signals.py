from .models import BookedUnit, Feedback, Lecture, LectureHall, Notification, RegisteredUnit
from django.db.models.signals import pre_save, post_save
from .utils import schedule_recurring_lectures
from datetime import datetime as dt
from django import dispatch
from random import sample
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
    current_day = dt.now().strftime('%Y-%m-%d')

    if instance.id == '':
        instance.id = str(uuid.uuid4()).replace('-', '')[:30]
    
    elif instance.lecture_hall is None:
        # Algorithm to assign lecture halls to a given lecture
        # 1. Get total number of students who have registered the unit, i.e. registered_students
        # 2. Get total number of students who will be attending the lecture, i.e. total_attendees
        # 3. Check if the lecture's "is_taught" is False
        # 4. Check if total_attendees > 0 and total_attendees <= registered_students
        # 5. If True, assign a lecture hall
        # 6. else do not assign a lecture hall, i.e pass
        # 7. If True, 
        #       - query for an empty lecture hall
        #       - check queried lecture halls with the seating capacity of atleast the total attendees or registered_students.
        # If lecture hall is found,
        #    - check if registered_students < LR_seating_capacity
        #    - if True, get number of registered_students
        #         - if number <= 20 assign discussion rooms, new building
        #         - if number <= 60 assign lecture rooms
        #         - if number <= 100 assign MPH

        registered_students = RegisteredUnit.objects.filter(unit=instance.unit_name, is_registered=True).count()   # total students who have registered the unit for current lecture
        total_attendees = Lecture.objects.filter(unit_name=instance.unit_name, is_attending=True).count()   # no. of students who will attend the lecture i.e. students who have confirmed attendance
        if instance.is_taught is False:
            if (total_attendees >= 0) and (total_attendees <= registered_students):
                lecture_halls = [hall.hall_no for hall in LectureHall.objects.all()]
                sampled_lr = sample(lecture_halls, 1)[0]    # sample lecture halls and pick the first lecture hall from the list
                
                if registered_students <= 20:
                    disc_rooms = [room.hall_no for room in LectureHall.objects.filter(hall_no__icontains='dr')]
                    sample_room = sample(disc_rooms, 1)[0]

                    check_lr_exists = Lecture.objects.filter(lecture_hall=disc_rooms, lecture_date=current_day, is_taught=False).exists()    # check if discussion room has been taken
                    if check_lr_exists is True:
                        _disc_rooms = [room.hall_no for room in LectureHall.objects.all().exclude(sample_room)]     # exclude the assigned/occupied disc_room
                        resample_rooms = sample(_disc_rooms, 1)[0]  # sample QS and get a new discussion room.
                        selected_disc_room = LectureHall.objects.get(hall_no=resample_rooms)     # get ID of the resampled discussion room
                        instance.lecture_hall = selected_disc_room
                    
                    else:
                        _room = LectureHall.objects.get(hall_no=sample_room)
                        instance.lecture_hall = _room
                
                elif registered_students <= 60:
                    _hall_id_ = LectureHall.objects.get(hall_no__icontains=sampled_lr)
                    get_scheduled_lec = Lecture.objects.filter(lecture_hall=_hall_id_, lecture_date=current_day, is_taught=False).exists()   # check if sampled lecture hall has been assigned to an existing scheduled lecture.

                    if get_scheduled_lec is True:
                        _lec_rooms_qs = [hall.hall_no for hall in LectureHall.objects.all().exclude(sampled_lr)]
                        resample_lrs = sample(_lec_rooms_qs, 1)[0]
                        selected_hall = LectureHall.objects.get(hall_no__icontains=resample_lrs)
                        instance.lecture_hall = selected_hall
                    
                    else:
                        instance.lecture_hall = _hall_id_

                elif registered_students <= 100:
                    _hall_id = LectureHall.objects.filter(hall_no__icontains='MPH')
                    instance.lecture_hall = _hall_id

                else:
                    pass

    # mark a given lecture as already taught, i.e. lecture has been taught
    elif instance.is_taught is False:   # check if is_taught is False in the current instance
        current_date = dt.now()
        if (current_date.hour >= instance.end_time.hour) and (instance.lecture_date.strftime('%Y-%m-%d') <= current_date.strftime('%Y-%m-%d')):
            instance.is_taught = True   # set "is_taught" to True

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
