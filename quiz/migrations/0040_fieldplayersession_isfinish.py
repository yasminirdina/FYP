# Generated by Django 3.2.2 on 2021-09-17 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0039_alter_fieldplayersession_timetaken'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldplayersession',
            name='isFinish',
            field=models.BooleanField(default=False),
        ),
    ]