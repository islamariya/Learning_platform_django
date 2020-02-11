from django.contrib import admin

from .models import CourseCategories, Course, CourseStudyPlan, Homework, CourseFlows, StudentsAcademicPerformance, \
                     CourseFlowTimetable, StudentsInCourseFlow


@admin.register(CourseCategories)
class CourseCateroiesAdmin(admin.ModelAdmin):
    list_display = ['category_title', 'is_category_active']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_title', 'category', 'is_course_active', 'course_version']
    ordering = ('category', 'course_title', '-course_version')
    search_fields = ('course_title', 'category')
    list_filter = ['category', 'is_course_active']
    save_as = True


@admin.register(CourseStudyPlan)
class CourseStudyPlan(admin.ModelAdmin):
    list_display = ['course_attached', 'lesson_number', 'lesson_title']
    list_display_links = ('lesson_number', 'lesson_title')
    ordering = ('course_attached', 'lesson_number')
    list_filter = ['course_attached', 'course_attached__course_version', 'lesson_number']
    save_as = True


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['homework_title','homework_number', 'course_flow_attached']
    list_filter = ['course_flow_attached']
    ordering = ('course_flow_attached', 'homework_number')
    date_hierarchy = 'due_date'
    save_as = True


@admin.register(CourseFlows)
class CourseFlowsAdmin(admin.ModelAdmin):
    list_display = ['course', 'course_code', 'course_start_date', 'is_course_over']
    list_filter = ['course__category', 'course', 'is_course_over']
    ordering = ('course', '-course_start_date')
    date_hierarchy = 'course_start_date'
    search_fields = ('course',)
    save_as = True


@admin.register(StudentsInCourseFlow)
class StudentsInCourseFlow(admin.ModelAdmin):
    list_display = ['course_code', 'student', 'is_student_active']
    list_filter = ['course_code__course__category', 'course_code__course', 'course_code',
                   ('student', admin.RelatedOnlyFieldListFilter), 'is_student_active']
    search_fields = ('student',)
    save_as = True


@admin.register(StudentsAcademicPerformance)
class StudentsAcademicPerformanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'homework_id', 'homework_status']
    list_display_links = ['student', 'homework_id']
    list_filter = ['course_code__course', 'course_code', 'student', 'homework_id', 'homework_status']
    search_fields = ['student', 'homework_id']
    save_as = True


@admin.register(CourseFlowTimetable)
class CourseFlowTimetableAdmin(admin.ModelAdmin):
    list_display = ['course_flow', 'lesson_id', 'lesson_date']
    list_filter = ['course_flow', 'lesson_id']
    save_as = True
