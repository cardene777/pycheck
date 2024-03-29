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
        return str(self.question_number)


def translate(instance, filename):
    filename = ''.join(filename.split())
    from pykakasi import kakasi
    kakasi = kakasi()
    kakasi.setMode('H', 'a')
    kakasi.setMode('K', 'a')
    kakasi.setMode('J', 'a')
    conv = kakasi.getConverter()
    return f"images/{conv.do(filename)}"


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
        upload_to=translate,
        default="images/paiza.png"
    )

    def __str__(self):
        return str(self.username)


class Result(models.Model):
    class Meta:
        verbose_name = "成績"
        verbose_name_plural = '成績'

    username = models.CharField(
        verbose_name="ユーザー名",
        max_length=100
    )

    present_number = models.FloatField(
        verbose_name="提出数",
        default=0,
    )

    total_points = models.FloatField(
        verbose_name="合計点",
        default=0
    )

    average_point = models.FloatField(
        verbose_name="平均点",
        default=0
    )

    def __str__(self):
        return str(self.average_point)
