# Generated by Django 3.2.4 on 2022-02-04 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0014_alter_university_uni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]