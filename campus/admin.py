from .models import BookedUnit, Feedback, Lecture, LectureHall, RegisteredUnit
from django.contrib import admin

@admin.register(BookedUnit)
class BookedUnitsTable(admin.ModelAdmin):
    list_display = ['lecturer', 'course_name', 'year_of_study', 'semester']
    readonly_fields = ['lecturer', 'course_name', 'year_of_study', 'semester']

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
    # readonly_fields = ['academic_block', 'hall_no', 'seating_capacity', 'floor', 'rating']

@admin.register(Feedback)
class StudentsFeedbackTable(admin.ModelAdmin):
    list_display = ['lecture_hall', 'rate_score', 'date_posted']
    readonly_fields = ['lecture_hall', 'complaint', 'description', 'rate_score']
