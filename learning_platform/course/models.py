from django.db import models

from user_profile.models import MyUser


class CourseCategories(models.Model):
    """This models represents Course Categories, showing in main menu (like Programming, Marketing, DevOps, etc)"""
    category_title = models.CharField(max_length=70, unique=True, verbose_name='Название категории')
    category_slug = models.SlugField(max_length=200, unique=True, verbose_name='Слег')
    is_category_active = models.BooleanField(default=False, verbose_name='Активная категория')

    class Meta:
        verbose_name = 'Категори'
        verbose_name_plural = 'Категории'
        ordering = ["category_title"]

    def __str__(self):
        return self.category_title


class Course(models.Model):
    """This models represents information about Courses. Unactive course is not shown at the web-site but can be used
    to get some statistic data in reports.
    Each course has a version (integer: 1,2,3, etc) Please add a new version in case of serious modifications of
    course (like price changing).
    Course duration is a sting in format: "4 месяца, 4 академ. часа в неделю Пн 20:00, Чт 20:00".
    Each launch of course in represented in class CourseFlows. """
    course_title = models.CharField(max_length=70, blank=False, verbose_name='Наименование курса')
    course_slug = models.SlugField(max_length=200, verbose_name='Слег')
    is_course_active = models.BooleanField(default=False, verbose_name='Курс доступен')
    category = models.ForeignKey(CourseCategories, on_delete=models.CASCADE, related_name='categories',
                                 verbose_name='Категория')
    course_short_description = models.CharField(max_length=300, verbose_name='Краткое описание')
    course_overview = models.TextField(verbose_name='Описание')
    course_duration = models.CharField(max_length=100, verbose_name='Продолжительность')
    course_price = models.IntegerField(verbose_name='Цена')
    course_creation_date = models.DateField(auto_now_add=True)
    course_version = models.IntegerField(verbose_name='Версия курса')
    course_img = models.ImageField(upload_to='courses', null=True, blank=True, verbose_name='Изображение')


    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['course_title', ]

    def __str__(self):
        return f'{self.course_title} версия {self.course_version}'


class CourseStudyPlan(models.Model):
    """This class represents lessons, that should be taught in course. This models contains general information
    about lesson such as title, number in study plan, goals, version.
    Each lesson should be attached to specific version of course.
    Specific data like tutor, date will be provided in CourseFlowTimetable."""
    lesson_title = models.CharField(max_length=100, blank=False, verbose_name='Тема занятия')
    lesson_number = models.IntegerField(verbose_name='Порядковый Номер занятия в курсе')
    course_attached = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='study_plans',
                                        verbose_name='Курс')
    lesson_description = models.TextField(verbose_name='Описание занятия')
    is_lesson_active = models.BooleanField(verbose_name='Доступность', default=False)
    lesson_version = models.IntegerField(verbose_name='Версия урока', default=1)

    class Meta:
        verbose_name = 'Учебный план курса'
        verbose_name_plural = 'Учебные планы курсов'
        ordering = ['lesson_title']

    def __str__(self):
        return f'"{self.lesson_title}" курса "{self.course_attached}"'


class CourseFlows(models.Model):
    """This class represents each launch of course. Course code is should have a abbreviation of course tile and
    start date (like, PHP 10.2019) """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_flows', verbose_name='Курс')
    course_start_date = models.DateField(blank=False, verbose_name='Дата начала')
    course_curator = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='course_flows',
                                       verbose_name='Куратор')
    course_code = models.CharField(max_length=50, unique=True, verbose_name='Код потока')
    is_course_over = models.BooleanField(default=False, verbose_name='Поток завершен')

    class Meta:
        verbose_name = 'Поток (набор) курса'
        verbose_name_plural = 'Потоки курсов'
        ordering = ['course_start_date']

    def __str__(self):
        return f'{self.course} {self.course_start_date}'


class Homework(models.Model):
    """This class represents homework, that should be done during each course flow. """
    homework_title = models.CharField(verbose_name='Название', max_length=200, blank=False)
    homework_number = models.IntegerField(verbose_name='Порядковый номер в курсе', default=1)
    course_flow_attached = models.ForeignKey(CourseFlows, on_delete=models.CASCADE, related_name='homework',
                                             verbose_name='Поток курса')
    homework_description = models.TextField(verbose_name='Описание')
    due_date = models.DateField(verbose_name='Срок сдачи')
    is_homework_active = models.BooleanField(verbose_name='Доступность', default=False)

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'

    def __str__(self):
        return f'№{self.homework_number} {self.homework_title} {self.course_flow_attached}'


class StudentsInCourseFlow(models.Model):
    """This class represents Students in each Course Flow."""
    course_code = models.ForeignKey(CourseFlows, on_delete=models.CASCADE, related_name='students_in_flow',
                                    verbose_name='Поток курса')
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='students_in_flow',
                                verbose_name='Студент')
    start_learning_date = models.DateField(verbose_name='Дата начала обучения')
    is_student_active = models.BooleanField(default=True, verbose_name='Учится')

    class Meta:
        verbose_name = 'Студенты в потоке'
        verbose_name_plural = 'Студенты в потоке'

    def __str__(self):
        return f'{self.student} {self.course_code}'


class StudentsAcademicPerformance(models.Model):
    """This course represents information about each Student's academic performance.  """
    HOMEWORK_STATUS_CHOICES = (("NOT_DONE", "not done"),
                               ("ON_REVIEW", "on review"),
                               ("SEND_TO_REWORK", "send to rework"),
                               ("COMPLETE", "complete")
                               )
    course_code = models.ForeignKey(CourseFlows, on_delete=models.CASCADE, related_name='students_homework',
                                    verbose_name='Поток курса')
    student = models.ForeignKey(StudentsInCourseFlow, on_delete=models.CASCADE, related_name='students_homework',
                                verbose_name='Студент')
    homework_id = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='students_homework',
                                    verbose_name='Дом задание')
    date_of_completion = models.DateField(blank=True, null=True, verbose_name='Факт дата сдачи')
    homework_status = models.CharField(max_length=20, choices=HOMEWORK_STATUS_CHOICES, default="NOT_DONE",
                                       verbose_name='Статус работы')
    teacher_comments = models.TextField(blank=True, verbose_name='Комментарии преподавателя')

    class Meta:
        verbose_name = 'Успеваемость студентов'
        verbose_name_plural = 'Успеваемость студентов'

    def __str__(self):
        return f'Домашняя работа "{self.homework_id.homework_title}" Student {self.student.student.first_name}'


class CourseFlowTimetable(models.Model):
    """This class represents timetable of each Course Flow."""
    lesson_id = models.ForeignKey(CourseStudyPlan, on_delete=models.CASCADE, related_name='courseflow_timetable',
                                  verbose_name='Номер занятия')
    course_flow = models.ForeignKey(CourseFlows, on_delete=models.CASCADE, related_name='courseflow_timetable',
                                    verbose_name='Поток курса')
    lesson_date = models.DateTimeField(verbose_name='Дата занятия')
    lesson_teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Преподаватель')

    class Meta:
        verbose_name = 'Расписание занятий'
        verbose_name_plural = 'Расписание занятий'

    def __str__(self):
        return f"{self.lesson_id} {self.lesson_date}"
