# Generated by Django 3.2.4 on 2022-01-29 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pTest', '0007_auto_20220101_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='questionDesc',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
