from .forms import EditScheduledLectureForm, FeedbackForm, LecturerUnitsBookingForm, StudentsAttendanceConfirmationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import BookedUnit, Lecture, LectureHall, RegisteredUnit
from datetime import time, datetime as dt


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

        events = Lecture.objects.filter(
            lecturer__department=request.user.student.department,
            unit_name__students_course=request.user.student.course,
        )
        event_data = []
        for event in events:
            event_data.append({
                'title': str(event.unit_name),  # Use appropriate field from your Lecture model
                'start': event.lecture_date.strftime('%Y-%m-%d') + 'T' + event.start_time.strftime('%H:%M:%S'),
                'end': event.lecture_date.strftime('%Y-%m-%d') + 'T' + event.end_time.strftime('%H:%M:%S'),
            })
    
        context = {
            'TotalUnits': total_units,
            'TotalLectures': total_lectures,
            'scheduled_lectures': scheduled_lectures_QS,
            'events': event_data,
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
            year_of_study=request.user.student.year,
            semester=request.user.student.semester,
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
class StudentsLecturesDetailView(View):
    template_name = 'dashboard/students/lectures.html'
    def get(self, request, _student, *args, **kwargs):
        lectures_QS = Lecture.objects.filter(
            lecturer__department=request.user.student.department, unit_name__students_course=request.user.student.course,
        ).order_by('-lecture_date', '-start_time', 'unit_name')

        context = {'scheduled_lectures': lectures_QS}
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
        booked_units_QS = BookedUnit.objects.filter(lecturer=staff_id)

        context = {
            'booked_units': booked_units_QS,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, staff_id, staff_name, *args, **kwargs):
        booked_units_QS = BookedUnit.objects.filter(lecturer=staff_id)
        data_unit_name = request.POST.get('unit-name')
        data_lec_date = request.POST.get('lecture-date')
        data_start_time = request.POST.get('start-time')
        data_end_time = request.POST.get('end-time')
        data_pattern = request.POST.get('recurrence-pattern')

        # datetime() and time() have parameters. In this case we have to assign this parameters values from a HTML form.
        # datetime() which in this case, is renamed to dt, has parameters - year, month, day
        # time() has parameters - hour, minute
        lecture_scheduled_date = dt(year=int(data_lec_date[:4]), month=int(data_lec_date[5:7]), day=int(data_lec_date[-2:]))  # assign year, month, day from the HTML form input type="date"
        lecture_start_time = time(hour=int(data_start_time[:2]), minute=int(data_start_time[-2:]))  # hour and minute of the scheduled lecture
        lecture_end_time = time(hour=int(data_end_time[:2]), minute=int(data_end_time[-2:]))    # end hour and minute of the scheduled lecture.

        # A scheduled lecture SHOULD range from the current date to two weeks i.e. 14 days from the current date.
        # For example, if a lecture is scheduled to be taught on Nov. 20, 2023 it should be in the range of current date, Nov. 14, 2023 - Nov. 28, 2023.
        if (lecture_scheduled_date.strftime('%Y-%m-%d') < dt.now().strftime("%Y-%m-%d")) or (elapsed_days:=(lecture_scheduled_date.day - dt.now().day)) > 14:
            messages.error(request, 'Invalid date input! Date should range from current date to 14 days after current date.')
        
        elif (str(lecture_start_time) < dt.now().strftime("%H:%M")) or ():
            messages.error(request, 'Invalid time input! Enter time ahead of current time.')

        elif lecture_end_time > lecture_start_time:   # check if the end_time is greater than start_time.
            time_difference_hours = lecture_end_time.hour - lecture_start_time.hour
            time_difference_minutes = lecture_end_time.minute - lecture_start_time.minute

            # adjust for negative values.
            if time_difference_minutes < 0:
                time_difference_minutes += 60
                time_difference_hours -= 1
            
            # check if time is less than 30 minutes.
            if time_difference_hours == 0 or time_difference_minutes < 30:
                messages.error(request, 'Time too short! Time should range between 30 minutes and 3 hours.')

            elif time_difference_hours > 3:
                messages.error(request, 'A lecture MUST be 3 hours maximum!')
            
        else:
            unit_obj = BookedUnit.objects.get(id=data_unit_name)

            new_scheduled_lecture = Lecture.objects.create(
                lecturer=request.user.faculty,
                unit_name=unit_obj,
                lecture_date=data_lec_date,
                start_time=data_start_time,
                end_time=data_end_time,
                recurrence_pattern=data_pattern,
            )
            new_scheduled_lecture.save()

            messages.success(request, 'Lecture successfully scheduled!')
            return redirect('schedule_lecture', staff_id, staff_name)
        
        context = {'booked_units': booked_units_QS,}
        return render(request, self.template_name, context)

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
    