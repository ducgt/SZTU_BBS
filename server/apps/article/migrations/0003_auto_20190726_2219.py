# Generated by Django 2.2 on 2019-07-26 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('article', '0002_auto_20190726_0941'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='data',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='publish_data',
            new_name='publish_date',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='in_topic',
        ),
        migrations.RemoveField(
            model_name='topic_image',
            name='image_7',
        ),
        migrations.RemoveField(
            model_name='topic_image',
            name='image_8',
        ),
        migrations.RemoveField(
            model_name='topic_image',
            name='image_9',
        ),
        migrations.AddField(
            model_name='reply',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='该回复的主人是否已读'),
        ),
        migrations.AddField(
            model_name='topic',
            name='to_top',
            field=models.BooleanField(default=False, verbose_name='是否置顶'),
        ),
        migrations.AlterField(
            model_name='session',
            name='article_counts',
            field=models.IntegerField(default=0, verbose_name='板块文章总数'),
        ),
        migrations.AlterField(
            model_name='session',
            name='name',
            field=models.CharField(max_length=16, unique=True, verbose_name='板块名'),
        ),
        migrations.AlterField(
            model_name='session',
            name='self_counts',
            field=models.IntegerField(default=0, verbose_name='板块点击数'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='great_counts',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='reply_counts',
            field=models.IntegerField(default=0, verbose_name='话题回复数'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='self_counts',
            field=models.IntegerField(default=0, verbose_name='话题点击数'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100, verbose_name='评论内容')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('image', models.ImageField(default='', null=True, upload_to='Reply/%Y%m%d', verbose_name='评论图片')),
                ('to_top', models.BooleanField(default=False, verbose_name='是否置顶')),
                ('is_read', models.BooleanField(default=False, verbose_name='该话题的主人是否已读')),
                ('in_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Topic', verbose_name='所在话题')),
                ('replyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='评论者')),
            ],
            options={
                'verbose_name': '回复',
                'verbose_name_plural': '回复',
            },
        ),
        migrations.AddField(
            model_name='reply',
            name='in_comment',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='article.Comment', verbose_name='所在评论'),
        ),
    ]
