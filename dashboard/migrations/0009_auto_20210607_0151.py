# Generated by Django 3.2.2 on 2021-06-06 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20210601_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeroomteacherclass',
            name='teacherID',
            field=models.ForeignKey(default='NA', on_delete=django.db.models.deletion.SET_DEFAULT, to='dashboard.teacher'),
        ),
        migrations.AlterField(
            model_name='student',
            name='parentID',
            field=models.ForeignKey(default='NA', on_delete=django.db.models.deletion.SET_DEFAULT, to='dashboard.parent'),
        ),
        migrations.AlterField(
            model_name='student',
            name='studentClass',
            field=models.ForeignKey(default='NA', on_delete=django.db.models.deletion.SET_DEFAULT, to='dashboard.homeroomteacherclass'),
        ),
    ]
