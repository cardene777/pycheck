from django.db import models
from django.utils import timezone


# Create your models here.

class QuestionModel(models.Model):
    class Meta:
        verbose_name = "質問掲示板"
        verbose_name_plural = '質問掲示板'

    CATEGORY_CHOICES = (
        (1, 'エラー対処'),
        (2, '技術質問'),
    )

    LEVEL_CHOICES = (
        (1, 'より深く'),
        (2, '対処法のみ'),
    )

    title = models.CharField(
        verbose_name="質問タイトル",
        max_length=50,
        blank=False
    )
    content = models.TextField(
        verbose_name="質問内容",
        blank=False,
    )

    idea = models.TextField(
        verbose_name="自分の認識or行った対処法",
        blank=False,
    )

    create = models.DateTimeField(
        verbose_name="作成日",
        default=timezone.now,
    )

    # 質問カテゴリ
    category = models.IntegerField(
        verbose_name="質問カテゴリ",
        choices=CATEGORY_CHOICES,
        blank=False,
    )

    # して欲しい回答のやり方
    level = models.IntegerField(
        verbose_name="回答レベル",
        choices=LEVEL_CHOICES,
        blank=True,
    )

    # 画像
    image_1 = models.ImageField(
        verbose_name='画像1',
        upload_to='media/',
        blank=True,
        null=True,
    )

    image_2 = models.ImageField(
        verbose_name='画像2',
        upload_to='media/',
        blank=True,
        null=True,
    )

    image_3 = models.ImageField(
        verbose_name='画像3',
        upload_to='media/',
        blank=True,
        null=True,
    )

    image_4 = models.ImageField(
        verbose_name='画像4',
        upload_to='media/',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.title} {self.content} {self.idea} {self.create} {self.category} {self.level} \
        {self.image_1} {self.image_2} {self.image_3} {self.image_4}"


# コメント機能
class Comment(models.Model):
    comment = models.TextField(default="")

    created_at = models.DateTimeField(auto_now_add=True)

    article = models.ForeignKey(to=QuestionModel, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
