from campus.models import Lecture, Notification
from accounts.models import User
from datetime import datetime as dt


def user_notifications(request):
    """ This function is used to display user notifications in all templates. """
    current_date = dt.now().strftime('%Y-%m-%d')
    student_notifications = []
    lecturer_notifications = []
    total_lec_notifications = 0
    total_stud_notifications = 0
    
    if request.user.is_anonymous is False and request.user.is_superuser is False:  # check if user is anonymous
        try:
            lecturer_notifications = Notification.objects.filter(
                scheduled_lecture__lecturer=request.user.faculty,
                date_created__date=current_date,
            ).order_by('date_created') if str(request.user) == str(request.user.faculty) else []    # if logged in user is lec/HOD return notifications else return empty list
            total_lec_notifications = lecturer_notifications.count() if len(lecturer_notifications) > 0 else total_lec_notifications

        except:
            student_notifications = Notification.objects.filter(
                scheduled_lecture__student=request.user.student,
                date_created__date=current_date,
            ).order_by('date_created') if str(request.user) == str(request.user.student) else []    # if logged in user is student return notifications else return empty list
            total_stud_notifications = student_notifications.count() if len(student_notifications) > 0 else total_stud_notifications
            
    context = {
        'student_notifications': student_notifications,
        'lecturer_notifications': lecturer_notifications,
        'TotalStudentNotifications': total_stud_notifications,
        'TotalLecturerNotifications': total_lec_notifications,
    }
    return context