# Generated by Django 3.2.4 on 2021-12-08 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_auto_20211102_2119'),
        ('pTest', '0002_auto_20211206_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('ID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='dashboard.student')),
            ],
        ),
        migrations.DeleteModel(
            name='StudentTestResult',
        ),
    ]
