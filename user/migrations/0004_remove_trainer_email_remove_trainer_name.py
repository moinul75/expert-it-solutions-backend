# Generated by Django 5.1 on 2024-09-07 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_student_class_days_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='trainer',
            name='name',
        ),
    ]
