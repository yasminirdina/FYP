# Generated by Django 3.2.2 on 2022-01-02 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_auto_20211224_2105'),
        ('dashboard', '0030_notification_recipientid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='blogCommentReplyID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_reply_notif_for', to='blog.blogpostcomment'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='blogPostCommentID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_notif_for', to='blog.blogpostcomment'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='blogPostID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_notif_for', to='blog.blogpost'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='messageID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_notif_for', to='dashboard.message'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='suggestionID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggestion_notif_for', to='dashboard.suggestion'),
        ),
    ]
