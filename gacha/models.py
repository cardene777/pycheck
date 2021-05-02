from django.db import models


class GachaTitle(models.Model):
    class Meta:
        verbose_name = "ガチャタイトル"
        verbose_name_plural = 'ガチャタイトル'

    title = models.CharField(
        verbose_name="ガチャタイトル",
        max_length=100,
    )

    image = models.ImageField(
        verbose_name="タイトル画像",
        upload_to="images/",
        default="paiza.png"
    )

    def __str__(self):
        return str(self.title)


class GachaItem(models.Model):
    class Meta:
        verbose_name = "ガチャアイテム"
        verbose_name_plural = 'ガチャアイテム'

    RARE = (
        ("VR", "バンタン限定"),
        ("SR", "スーパーレア"),
        ("R", "レア"),
        ("N", "ノーマル"),
    )

    title = models.ForeignKey(
        GachaTitle,
        verbose_name="ガチャタイトル",
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name="キャラクター名",
        max_length=100,
    )

    rare = models.CharField(
        verbose_name="レア度",
        max_length=10,
        choices=RARE,
        default="N",
    )

    image = models.ImageField(
        verbose_name="アイテム画像",
        upload_to="images/",
        default="paiza.png"
    )

    def __str__(self):
        return f"{str(self.title)} {str(self.name)}"


class Count(models.Model):
    class Meta:
        verbose_name = "ガチャカウンター"
        verbose_name_plural = 'ガチャカウンター'

    username = models.CharField(
        verbose_name="ユーザー名",
        max_length=100,
    )

    counter = models.IntegerField(
        verbose_name="ガチャカウント",
        default=0,
    )

    def __str__(self):
        return f"{str(self.username)} {self.counter}"
