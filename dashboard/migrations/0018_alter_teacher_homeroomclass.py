# Generated by Django 3.2.2 on 2021-06-13 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_classlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='homeroomClass',
            field=models.CharField(choices=[('NA', 'NA'), ('5 ARIF', '5 ARIF'), ('5 BESTARI', '5 BESTARI'), ('5 CENDEKIA', '5 CENDEKIA')], default='NA', max_length=25),
        ),
    ]
