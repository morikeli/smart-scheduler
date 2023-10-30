from .models import BookedUnit, Faculty, Feedback, Lecture, LectureHall, RegisteredUnit, School, Student
from django.contrib import admin

@admin.register(School)
class SchoolsRecordsTable(admin.ModelAdmin):
    list_display = ['name', 'total_students', 'total_staff']
    readonly_fields = ['name', 'total_students', 'total_staff']

@admin.register(Student)
class StudentsDetailsTable(admin.ModelAdmin):
    list_display = ['student_name', 'school', 'programme', 'year', 'semester']
    readonly_fields = ['student_name', 'school', 'programme', 'year', 'semester']

@admin.register(Faculty)
class FacultyRecords(admin.ModelAdmin):
    list_display = ['staff', 'department', 'position']
    readonly_fields = ['staff', 'department', 'position']

@admin.register(BookedUnit)
class BookedUnitsTable(admin.ModelAdmin):
    list_display = ['lecturer', 'course_code', 'course_title']
    readonly_fields = ['lecturer', 'course_code', 'course_title']

@admin.register(RegisteredUnit)
class RegisteredUnitsRecords(admin.ModelAdmin):
    list_display = ['student', 'unit', 'is_registered']
    readonly_fields = ['student', 'unit', 'is_registered']

@admin.register(Lecture)
class ScheduledLecturesTable(admin.ModelAdmin):
    list_display = ['lecturer', 'lecture_hall', 'lecture_date', 'total_students', 'is_taught']
    readonly_fields = ['lecturer', 'lecture_hall', 'lecture_date', 'start_time', 'end_time', 'total_students', 'is_taught']

@admin.register(LectureHall)
class LectureHallsRecords(admin.ModelAdmin):
    list_display = ['academic_block', 'hall_no', 'seating_capacity', 'floor', 'rating']
    readonly_fields = ['academic_block', 'hall_no', 'seating_capacity', 'floor', 'rating']

@admin.register(Feedback)
class StudentsFeedbackTable(admin.ModelAdmin):
    list_display = ['student', 'lecture_hall', 'rate_score']
    readonly_fields = ['student', 'lecture_hall', 'complaint', 'description', 'rate_score']
