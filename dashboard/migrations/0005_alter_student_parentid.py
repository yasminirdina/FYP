# Generated by Django 3.2.2 on 2021-05-24 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_student_parentid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='parentID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.parent'),
        ),
    ]
