# Generated by Django 3.2.2 on 2021-12-15 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_alter_homeroomteacherclass_lastdateedited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='homeroomClass',
            field=models.CharField(choices=[('5 ARIF', '5 ARIF'), ('5 BESTARI', '5 BESTARI'), ('5 CENDEKIA', '5 CENDEKIA'), ('NA', 'NA')], default='NA', max_length=25),
        ),
    ]
