# Generated by Django 3.2.2 on 2021-06-07 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_alter_teacher_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='homeroomClass',
            field=models.CharField(choices=[('NA', 'NA'), ('5 ARIF', '5 ARIF'), ('5 BESTARI', '5 BESTARI'), ('5 CENDEKIA', '5 CENDEKIA'), ('5 DINAMIK', '5 DINAMIK')], default='NA', max_length=25),
        ),
    ]
