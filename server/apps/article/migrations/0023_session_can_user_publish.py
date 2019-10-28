# Generated by Django 2.2 on 2019-08-13 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0022_session_model_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='can_user_publish',
            field=models.BooleanField(default=False, verbose_name='用户是否可以在该版块发布(管理员可发布)'),
        ),
    ]
