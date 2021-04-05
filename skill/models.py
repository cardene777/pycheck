from django.db import models


class SkillCheckData(models.Model):
    class Meta:
        verbose_name = "画像データ"
        verbose_name_plural = '画像データ'

    username = models.CharField(
        verbose_name="ユーザー名",
        max_length=100
    )

    question_number = models.CharField(
        verbose_name="問題番号",
        max_length=20,
    )

    question_level = models.CharField(
        verbose_name="問題レベル",
        max_length=1
    )

    answer_time = models.CharField(
        verbose_name="回答時間",
        max_length=20,
    )

    score = models.IntegerField(
        verbose_name="点数",
        default=0,
    )

    def __str__(self):
        return f"{self.id} {self.username} {self.question_number} {self.question_level} " \
               f"{self.answer_time} {self.score}"


class Image(models.Model):
    class Meta:
        verbose_name = "画像"
        verbose_name_plural = '画像'

    username = models.CharField(
        verbose_name="ユーザー名",
        max_length=100,
        default="admin"
    )
    image = models.ImageField(
        verbose_name="画像",
        upload_to='',
        default="paiza.png"
    )

    def __str__(self):
        return self.image
