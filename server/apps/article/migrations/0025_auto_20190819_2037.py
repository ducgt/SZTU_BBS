# Generated by Django 2.2 on 2019-08-19 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0024_session_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='color',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='版块颜色'),
        ),
    ]