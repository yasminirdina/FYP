# Generated by Django 3.2.4 on 2022-02-01 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0009_jobs'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='course_id',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
