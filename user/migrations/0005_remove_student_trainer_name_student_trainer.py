# Generated by Django 5.1 on 2024-09-07 12:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_trainer_email_remove_trainer_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='trainer_name',
        ),
        migrations.AddField(
            model_name='student',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students_trainer', to='user.trainer'),
        ),
    ]
