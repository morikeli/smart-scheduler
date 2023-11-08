from .forms import EditScheduledLectureForm, FeedbackForm, LecturerUnitsBookingForm, StudentsAttendanceConfirmationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import BookedUnit, Lecture, LectureHall, RegisteredUnit
from accounts.models import Faculty
from datetime import datetime as dt

# students views
@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: (user.is_staff is False or user.is_superuser is False) and user.is_student is True), name='get')
class StudentHomepageView(View):
    form_class = StudentsAttendanceConfirmationForm
    template_name = 'dashboard/students/homepage.html'

    def get(self, request, *args, **kwargs):
        total_units = RegisteredUnit.objects.filter(student=request.user.student).count()
        total_lectures = Lecture.objects.filter(
            lecturer__department=request.user.student.department,
            lecture_date=dt.now().strftime('%Y-%m-%d'),
        ).count()
        
        scheduled_lectures_QS = Lecture.objects.filter(
            lecturer__department=request.user.student.department,
            unit_name__students_course=request.user.student.course,
        ).order_by('-lecture_date', '-start_time', 'unit_name')

        context = {
            'TotalUnits': total_units,
            'TotalLectures': total_lectures,
            'scheduled_lectures': scheduled_lectures_QS,
        }
        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: (user.is_staff is False or user.is_superuser is False) and user.is_student is True), name='get')
class StudentsUnitsRegistrationView(View):
    template_name = 'dashboard/students/register-units.html'

    def get(self, request, student_id, *args, **kwargs):
        units_QS = BookedUnit.objects.filter(
            lecturer__department=request.user.student.department,
            students_course=request.user.student.course,
        )
        reg_units_QS = RegisteredUnit.objects.filter(student=request.user.student)

        context = {
            'booked_units': units_QS,
            'registered_units': reg_units_QS,
        }
        return render(request, self.template_name, context)

    def post(self, request, student_id, *args, **kwargs):
        get_unit_field = request.POST.get('register-unit')

        unit_obj = BookedUnit.objects.get(id=get_unit_field)
        try:
            get_reg_unit = RegisteredUnit.objects.filter(unit=unit_obj).exists()
            if get_reg_unit is True:
                messages.warning(request, 'Selected unit already registered!')
                return redirect('unit_registration', student_id)
        
        except RegisteredUnit.DoesNotExist:
            register_unit = RegisteredUnit.objects.get_or_create(
                unit=unit_obj,
                student=request.user.student,
                is_registered=True,
            )

            messages.success(request, 'Unit successfully registered!')
            return redirect('unit_registration', student_id)
        
        return render(request, self.template_name)

@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: (user.is_staff is False or user.is_superuser is False) and user.is_student is True), name='get')
class LectureAttendanceConfiramtionView(View):
    form_class = StudentsAttendanceConfirmationForm
    template_name = 'dashboard/students/confirm-attendance.html'

    def get(self, request, lecture_id, _student, *args, **kwargs):
        lec_obj = Lecture.objects.get(id=lecture_id)
        form = self.form_class(instance=lec_obj)
        scheduled_lectures_QS = Lecture.objects.filter(
            lecturer__department=request.user.student.department,
            unit_name__students_course=request.user.student.course,
            student=None,
        ).order_by('-lecture_date', '-start_time', 'unit_name')


        context = {
            'AttendanceConfirmationForm': form,
            'scheduled_lectures': scheduled_lectures_QS,
            'lec_obj': lec_obj,

        }
        return render(request, self.template_name, context)

    def post(self, request, lecture_id, _student, *args, **kwargs):
        scheduled_lectures_QS = Lecture.objects.filter(
            lecturer__department=request.user.student.department,
            unit_name__students_course=request.user.student.course,
            student=None,
        ).order_by('-lecture_date', '-start_time', 'unit_name')
        
        lec_obj = Lecture.objects.get(id=lecture_id)        
        form = self.form_class(request.POST, instance=lec_obj)
        
        if form.is_valid():
            confirmation = form.save(commit=False)
            confirmation.student = request.user.student
            confirmation.total_students += 1
            confirmation.save()

            messages.success(request, 'Confirmation submitted succesfully!')
            return redirect('confirm_attendance', lecture_id, _student)

        context = {
            'AttendanceConfirmationForm': form,
            'scheduled_lectures': scheduled_lectures_QS,
            'lec_obj': lec_obj,
        
        }
        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: (user.is_staff is False or user.is_superuser is False) and user.is_student is True), name='get')
class SubmitFeedbackView(View):
    form_class = FeedbackForm
    template_name = 'students/feedback.html'

    def get(self, request, hall_id, *args, **kwargs):
        lecture_hall = LectureHall.objects.get(id=hall_id)
        form = self.form_class()

        context = {'FeedbackForm': form}
        return render(request, self.template_name, context)
    
    def post(self, request, hall_id, *args, **kwargs):
        lecture_hall = LectureHall.objects.get(id=hall_id)
        form = self.form_class(request.POST)

        if form.is_valid():
            new_feedback = form.save(commit=False)
            new_feedback.student = request.user
            new_feedback.lecture_hall = lecture_hall
            new_feedback.save()

            messages.info(request, 'Thank you for your feedback!')
            return redirect('give_feedback', hall_id)

        context = {'FeedbackForm': form}
        return render(request, self.template_name, context)

# faculty views
@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: (user.is_staff is False or user.is_superuser is False) and user.is_student is False), name='get')
class FacultyDashboardView(View):
    template_name = 'dashboard/faculty/homepage.html'

    def get(self, request, *args, **kwargs):
        total_booked_units = BookedUnit.objects.filter(lecturer=request.user.faculty).count()
        scheduled_lectures_QS = Lecture.objects.filter(lecturer=request.user.faculty).order_by('unit_name')

        context = {
            'TotalBookedUnits': total_booked_units,
            'scheduled_lectures': scheduled_lectures_QS,

        }
        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: (user.is_staff is False or user.is_superuser is False) and user.is_student is False), name='get')
class ScheduleLectureView(View):
    template_name = 'dashboard/faculty/schedule-lecture.html'

    def get(self, request, staff_id, staff_name, *args, **kwargs):
        booked_units_QS = BookedUnit.objects.filter(lecturer=request.user.faculty)

        context = {
            'booked_units': booked_units_QS,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, staff_id, staff_name, *args, **kwargs):
        data_unit_name = request.POST.get('unit-name')
        data_lec_date = request.POST.get('lecture-date')
        data_start_time = request.POST.get('start-time')
        data_end_time = request.POST.get('end-time')
        data_pattern = request.POST.get('recurrence-pattern')

        unit_obj = BookedUnit.objects.get(id=data_unit_name)
        new_scheduled_lecture = Lecture.objects.create(
            lecturer=request.user.faculty,
            unit_name=unit_obj,
            lecture_date=data_lec_date,
            start_time=data_start_time,
            end_time=data_end_time,
            recurrence_pattern=data_pattern,

        ).save()
        
        messages.success(request, 'Lecture successfully scheduled!')
        return redirect('schedule_lecture', staff_id, staff_name)

@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: (user.is_staff is False or user.is_superuser is False) and user.is_student is False), name='get')
class AssignUnitsforLecturersView(View):
    form_class = LecturerUnitsBookingForm
    template_name = 'dashboard/faculty/book-units.html'

    def get(self, request, staff_id, *args, **kwargs):
        booked_units_QS = BookedUnit.objects.filter(lecturer__department=request.user.faculty.department)
        form = self.form_class()

        context = {
            'LecturersUnitsBookingForm': form,
            'booked_units': booked_units_QS
        }
        return render(request, self.template_name, context)
    
    def post(self, request, staff_id, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            
            messages.info(request, 'Unit assigned to lecturer successfully!')
            return redirect('assign_units', staff_id)

        context = {'LecturersUnitsBookingForm': form}
        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: (user.is_staff is False or user.is_superuser is False) and user.is_student is False), name='get')
class LecturesDetailView(View):
    template_name = 'dashboard/faculty/lectures.html'

    def get(self, request, staff_name, staff_id, *args, **kwargs):
        scheduled_lectures_QS = Lecture.objects.filter(lecturer=request.user.faculty).order_by('unit_name')

        context = {
            'scheduled_lectures': scheduled_lectures_QS,

        }
        return render(request, self.template_name, context)
    
    def post(self, request, staff_name, staff_id, *args, **kwargs):
        lecture_record_ID = request.POST.get('scheduled-lecture')
        scheduled_lectures_QS = Lecture.objects.get(id=lecture_record_ID)
        scheduled_lectures_QS.delete()

        messages.error(request, 'You deleted a scheduled lecture!')
        return redirect('lectures_records', staff_name, staff_id)

@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: (user.is_staff is False or user.is_superuser is False) and user.is_student is False), name='get')
class EditScheduledLecturesView(View):
    form_class = EditScheduledLectureForm
    template_name = 'dashboard/faculty/edit.html'

    def get(self, request, staff_id, lecture_id, *args, **kwargs):
        lectures_QS = Lecture.objects.get(id=lecture_id)
        form = self.form_class(instance=lectures_QS)

        context = {
            'EditScheduledLectureForm': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, staff_id, lecture_id, *args, **kwargs):
        lectures_QS = Lecture.objects.get(id=lecture_id)
        form = self.form_class(request.POST, instance=lectures_QS)

        if form.is_valid():
            form.save()

            messages.warning(request, 'You updated a scheduled lecture!')
            return redirect('lectures_records', staff_id, request.user.faculty)

        context = {
            'EditScheduledLectureForm': form,
        }
        return render(request, self.template_name, context)
    