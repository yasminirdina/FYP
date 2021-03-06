# Generated by Django 3.2.4 on 2022-01-01 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pTest', '0006_auto_20211218_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentpersonalitysession',
            old_name='currentSectionScore',
            new_name='aSecScore',
        ),
        migrations.RemoveField(
            model_name='studentpersonalitysession',
            name='personalityID',
        ),
        migrations.AddField(
            model_name='studentpersonalitysession',
            name='cSecScore',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentpersonalitysession',
            name='eSecScore',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentpersonalitysession',
            name='iSecScore',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentpersonalitysession',
            name='rSecScore',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentpersonalitysession',
            name='sSecScore',
            field=models.IntegerField(default=0),
        ),
    ]
