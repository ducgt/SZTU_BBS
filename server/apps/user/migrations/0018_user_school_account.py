# Generated by Django 2.2 on 2019-08-14 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_user_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='school_account',
            field=models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='学号'),
        ),
    ]
