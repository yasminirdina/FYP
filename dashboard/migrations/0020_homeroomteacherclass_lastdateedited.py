# Generated by Django 3.2.2 on 2021-12-15 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_auto_20211102_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeroomteacherclass',
            name='lastDateEdited',
            field=models.DateField(auto_now=True),
        ),
    ]