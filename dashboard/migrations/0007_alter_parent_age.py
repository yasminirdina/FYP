# Generated by Django 3.2.2 on 2021-05-27 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_student_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='age',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
