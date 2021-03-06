# Generated by Django 3.1.6 on 2021-02-22 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('moodle', '0001_initial'), ('moodle', '0002_auto_20210221_1908'), ('moodle', '0003_delete_teacher'), ('moodle', '0004_auto_20210221_1933'), ('moodle', '0005_auto_20210221_2105'), ('moodle', '0006_auto_20210221_2118'), ('moodle', '0007_auto_20210222_1409'), ('moodle', '0008_auto_20210222_1409')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('creation_date', models.DateField(default=django.utils.timezone.now)),
                ('students', models.ManyToManyField(related_name='courses_learned', to=settings.AUTH_USER_MODEL)),
                ('teachers', models.ManyToManyField(related_name='courses_teached', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('modification_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='moodle.course')),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('ask_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('answer_date', models.DateTimeField(blank=True, null=True)),
                ('answerer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions_answered', to=settings.AUTH_USER_MODEL)),
                ('asker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_asked', to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='moodle.lesson')),
                ('answer_text', models.TextField(blank=True)),
                ('answered', models.BooleanField(default=False)),
            ],
        ),
    ]
