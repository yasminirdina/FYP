# Generated by Django 3.2.2 on 2021-06-07 07:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20210607_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeroomteacherclass',
            name='year',
            field=models.IntegerField(default=2021, validators=[django.core.validators.MinValueValidator(2021), django.core.validators.MaxValueValidator(2021)]),
        ),
        migrations.AddField(
            model_name='teacher',
            name='year',
            field=models.IntegerField(default=2021, validators=[django.core.validators.MinValueValidator(2021), django.core.validators.MaxValueValidator(2021)]),
        ),
        migrations.AlterField(
            model_name='homeroomteacherclass',
            name='className',
            field=models.CharField(default='NA', max_length=25, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.IntegerField(default=2021, validators=[django.core.validators.MinValueValidator(2021), django.core.validators.MaxValueValidator(2021)]),
        ),
    ]
