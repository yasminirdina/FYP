# Generated by Django 3.2.2 on 2021-12-02 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_blogpost_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='lastDateEdited',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='lastTimeEdited',
            field=models.TimeField(),
        ),
    ]
