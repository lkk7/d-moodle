# Generated by Django 3.1.6 on 2021-02-24 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0001_initial_squashed_0008_auto_20210222_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(max_length=1000),
        ),
    ]
