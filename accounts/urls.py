from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/<str:staff_name>/faculty/', views.EditFacultyStaffProfileView.as_view(), name='faculty_profile'),
    path('profile/<str:_student_name>/student/', views.EditStudentProfileView.as_view(), name='student_profile'),
    path('logout/', views.LogoutUserView.as_view(), name='logout_user'),

]