# Generated by Django 3.2.4 on 2022-01-31 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_alter_jobs_personality'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='admission',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='course',
            name='langguage',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='course',
            name='studyLevel',
            field=models.CharField(default='', max_length=120),
        ),
    ]