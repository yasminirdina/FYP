# Generated by Django 3.2.2 on 2021-12-05 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20211202_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostcomment',
            name='childCommentID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='blog.blogpostcomment'),
        ),
        migrations.AlterField(
            model_name='blogpostcomment',
            name='parentCommentID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='blog.blogpostcomment'),
        ),
    ]
