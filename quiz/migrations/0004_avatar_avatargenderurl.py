# Generated by Django 3.2.2 on 2021-05-21 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20210521_0026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('careerName', models.CharField(max_length=50)),
                ('workplace', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AvatarGenderURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatarGender', models.CharField(max_length=6)),
                ('imageURL', models.URLField()),
                ('avatarID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.avatar')),
            ],
        ),
    ]
