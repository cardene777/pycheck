# Generated by Django 3.1.2 on 2021-05-15 04:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='質問タイトル')),
                ('content', models.TextField(verbose_name='質問内容')),
                ('idea', models.TextField(verbose_name='自分の認識or行った対処法')),
                ('deadline', models.DateTimeField(default=django.utils.timezone.now, verbose_name='期日')),
                ('category', models.IntegerField(choices=[(1, 'エラー対処'), (2, '技術質問')], verbose_name='質問カテゴリ')),
                ('level', models.IntegerField(blank=True, choices=[(1, 'より深く'), (2, '対処法のみ')], verbose_name='回答レベル')),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='画像1')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='画像2')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='画像3')),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='画像4')),
            ],
            options={
                'verbose_name': '質問掲示板',
                'verbose_name_plural': '質問掲示板',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='question.questionmodel')),
            ],
        ),
    ]
