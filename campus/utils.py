from .models import Lecture, LectureHall, Notification, RegisteredUnit
from datetime import datetime as dt, timedelta, time
from django.http import HttpResponse
from django.db.models import Q
from time import sleep
import schedule


@schedule.repeat(schedule.every(1).minute.at(':15').until(time(17, 00)))
def schedule_recurring_lectures():
    """ This is a function that automatically schedules recurring lectures, i.e daily or weekly lectures. """

    recurring_classes = Lecture.objects.filter(Q(recurrence_pattern='daily') | Q(recurrence_pattern='weekly'))  # get recurring lectures
    current_day = dt.now().strftime('%A %b. %d, %Y')

    for _lecture in recurring_classes:
        # Check if today is the day for the recurring class
        if (current_day == _lecture.lecture_date.strftime('%A %b. %d, %Y')):
            # Code to notify participants (i.e. students)
            notification = Notification.objects.get_or_create(
                message=f'Lecture for unit "{_lecture.unit_name}" scheduled for today at {_lecture.start_time.strftime("%H:%M")}.',
                scheduled_lecture_id=_lecture.id,
            )

            # Code to adjust date and time for the next lectures
            if _lecture.recurrence_pattern == 'daily':
                schedule.repeat(schedule.every().minute.at(':15').until(time(17, 00)).do(schedule_recurring_lectures))
                # print(f'Time difference: {_lecture.start_time - timedelta(hours=3)}')
                # in daily lectures, we have to add 1 day to the current lecture date. For example,
                # if lecture_date is 2023-11-15 where 15 is the day, add 1 to 15 -> 15 + 1 = 16. Therefore,
                # the next scheduled class will be on date 2023-11-16
                # the timestamp, i.e. start_time & end_time, remains the same.
                Lecture.objects.update_or_create(
                    lecturer=_lecture.lecturer,
                    student=_lecture.student,
                    unit_name=_lecture.unit_name,
                    lecture_date=_lecture.lecture_date + timedelta(days=1),     # increment 1 day
                    start_time=_lecture.start_time,
                    end_time=_lecture.end_time,
                    recurrence_pattern=_lecture.recurrence_pattern,
                )
            
            elif _lecture.recurrence_pattern == 'weekly':
                # in weekly lectures, we have to add 7 days to the current lecture date. For example,
                # if lecture_date is 2023-11-15 where 15 is the day, add 7 to 15 -> 15 + 7 = 22. Therefore,
                # the next scheduled class will be on date 2023-11-22
                # the timestamp, i.e. start_time & end_time, remains the same.
                Lecture.objects.update_or_create(
                    lecturer=_lecture.lecturer,
                    student=_lecture.student,
                    unit_name=_lecture.unit_name,
                    lecture_date=_lecture.lecture_date + timedelta(days=7),    # add 7 days ahead of the lecture date
                    start_time=_lecture.start_time,
                    end_time=_lecture.end_time,
                    recurrence_pattern=_lecture.recurrence_pattern,
                )
            
            
            
            if len(recurring_classes) != 0:
                schedule.run_pending()
                sleep(1)   # 
