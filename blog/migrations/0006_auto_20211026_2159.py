# Generated by Django 3.2.2 on 2021-10-26 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='datePublished',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='lastDateEdited',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='lastTimeEdited',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='timePublished',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
