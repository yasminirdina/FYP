# Generated by Django 3.2.2 on 2021-06-14 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0029_auto_20210614_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='avatargenderimage',
            name='name',
            field=models.CharField(default='Tiada Ikon', max_length=50),
        ),
        migrations.AlterField(
            model_name='avatargenderimage',
            name='imageURL',
            field=models.URLField(),
        ),
    ]
