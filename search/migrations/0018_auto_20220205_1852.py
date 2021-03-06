# Generated by Django 3.2.4 on 2022-02-05 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0017_auto_20220204_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='contactInfo',
            field=models.CharField(blank=True, default='N/A', max_length=120),
        ),
        migrations.AddField(
            model_name='university',
            name='description',
            field=models.TextField(blank=True, default='N/A'),
        ),
        migrations.AddField(
            model_name='university',
            name='intStudent',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='university',
            name='linkPage',
            field=models.CharField(blank=True, default='N/A', max_length=120),
        ),
        migrations.AddField(
            model_name='university',
            name='location',
            field=models.CharField(blank=True, default='N/A', max_length=120),
        ),
        migrations.AddField(
            model_name='university',
            name='populatin',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='university',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='university',
            name='uniType',
            field=models.CharField(blank=True, default='N/A', max_length=120),
        ),
    ]
