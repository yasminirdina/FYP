# Generated by Django 3.2.2 on 2021-12-15 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_homeroomteacherclass_lastdateedited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeroomteacherclass',
            name='lastDateEdited',
            field=models.DateField(),
        ),
    ]