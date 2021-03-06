# Generated by Django 3.0.3 on 2020-02-19 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='Наименование курса')),
                ('slug', models.SlugField(max_length=200, verbose_name='Слег')),
                ('is_active', models.BooleanField(default=False, verbose_name='Курс доступен')),
                ('short_description', models.CharField(max_length=300, verbose_name='Краткое описание')),
                ('overview', models.TextField(verbose_name='Описание')),
                ('duration', models.CharField(max_length=100, verbose_name='Продолжительность')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('version', models.IntegerField(verbose_name='Версия курса')),
                ('main_img', models.ImageField(blank=True, null=True, upload_to='courses', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, unique=True, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Слег')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активная категория')),
            ],
            options={
                'verbose_name': 'Категори',
                'verbose_name_plural': 'Категории',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='CourseFlows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Код потока')),
                ('is_over', models.BooleanField(default=False, verbose_name='Поток завершен')),
            ],
            options={
                'verbose_name': 'Поток (набор) курса',
                'verbose_name_plural': 'Потоки курсов',
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='CourseFlowTimetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата занятия')),
            ],
            options={
                'verbose_name': 'Расписание занятий',
                'verbose_name_plural': 'Расписание занятий',
            },
        ),
        migrations.CreateModel(
            name='CourseLecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Тема занятия')),
                ('sequence_number', models.IntegerField(verbose_name='Порядковый Номер занятия в курсе')),
                ('description', models.TextField(verbose_name='Описание занятия')),
                ('is_active', models.BooleanField(default=False, verbose_name='Доступность')),
                ('version', models.IntegerField(default=1, verbose_name='Версия урока')),
            ],
            options={
                'verbose_name': 'Учебный план курса',
                'verbose_name_plural': 'Учебные планы курсов',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('sequence_number', models.IntegerField(default=1, verbose_name='Порядковый номер в курсе')),
                ('description', models.TextField(verbose_name='Описание')),
                ('due_date', models.DateField(verbose_name='Срок сдачи')),
                ('is_active', models.BooleanField(default=False, verbose_name='Доступность')),
            ],
            options={
                'verbose_name': 'Домашнее задание',
                'verbose_name_plural': 'Домашние задания',
            },
        ),
        migrations.CreateModel(
            name='StudentsEnrolled',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_learning_date', models.DateField(verbose_name='Дата начала обучения')),
                ('is_active', models.BooleanField(default=True, verbose_name='Учится')),
                ('course_flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students_in_flow', to='course.CourseFlows', verbose_name='Поток курса')),
            ],
            options={
                'verbose_name': 'Студенты в потоке',
                'verbose_name_plural': 'Студенты в потоке',
            },
        ),
        migrations.CreateModel(
            name='StudentsHomework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_completion', models.DateField(blank=True, null=True, verbose_name='Факт дата сдачи')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'not done'), (1, 'on review'), (2, 'send to rework'), (3, 'complete')], default=0, verbose_name='Статус работы')),
                ('teacher_comments', models.TextField(blank=True, verbose_name='Комментарии преподавателя')),
                ('course_flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students_homework', to='course.CourseFlows', verbose_name='Поток курса')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students_homework', to='course.Homework', verbose_name='Дом задание')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students_homework', to='course.StudentsEnrolled', verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Успеваемость студентов',
                'verbose_name_plural': 'Успеваемость студентов',
            },
        ),
    ]
