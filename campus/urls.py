from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.StudentHomepageView.as_view(), name='student_homepage'),
    path('units/<str:student_id>/register/', views.StudentsUnitsRegistrationView.as_view(), name='unit_registration'),
    path('lectures/<str:_student>/', views.StudentsLecturesDetailView.as_view(), name='student_lecture_records'),
    path('lecture/<str:lecture_id>/schedule/<str:_student>/confirm/', views.LectureAttendanceConfirmationView.as_view(), name='confirm_attendance'),
    path('halls/<str:hall_id>/feedback/', views.SubmitFeedbackView.as_view(), name='student_feedback'),
    
    path('dashboard/', views.FacultyDashboardView.as_view(), name='faculty_homepage'),
    path('<str:staff_id>/lecture/<str:staff_name>/schedule/', views.ScheduleLectureView.as_view(), name='schedule_lecture'),
    path('units/<str:staff_id>/book/', views.AssignUnitsforLecturersView.as_view(), name='assign_units'),
    path('<str:staff_id>/lectures/<str:staff_name>/records/', views.LecturesDetailView.as_view(), name='lectures_records'),
    path('<str:staff_id>/lecture/<str:lecture_id>/edit/', views.EditScheduledLecturesView.as_view(), name='edit_schedule'),

]
