from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator

class CdType(models.Model):
    name = models.CharField(
        "コンクールCDかその他のCDか",
        max_length=100,
    )
    created_at = models.DateTimeField(
        default=timezone.now,
    )

    def __str__(self):
        return self.name 


class Song(models.Model):
    title = models.CharField(
        "曲名", #管理画面で分かりやすくなる（verbose_nameとは別なので注意）
        max_length=200
    )
    composer = models.CharField(
        max_length=200
    )
    arranger = models.CharField(
        max_length=200,
        blank=True
    )
    artist = models.CharField(
        max_length=200
    )
    cd = models.CharField(
        max_length=200,
        blank=True,
    )
    cd_link = models.CharField(
        max_length=500,
    )
    cdYear = models.CharField( #この辺キャメルケースになってるけど正しい命名規則はアンダースコアなので今後は統一
        max_length=4,
        # validators=[MinLengthValidator(4)],
        blank=True,
    )
    cdVol = models.CharField(
        max_length=2,
        blank=True,
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        blank=True,
    )
    modified_at = models.DateTimeField(
        auto_now=timezone.now,
        blank=True,
    )
    cd_type = models.ForeignKey(
        CdType,
        verbose_name="CDタイプ",
        on_delete=models.PROTECT,
        default="1",
        blank=True,
    )
    asin = models.CharField(
        max_length=10,
        blank=True,
    )

    # class Meta:
    #     ordering = ('title',)
        # get_querysetでorder_byするのとどう違う？

    def __str__(self):
        return self.title 


class Comment(models.Model):
    name = models.CharField(
        "おなまえ",
        max_length=32,
        default="名無し"
        )
    text = models.TextField(
        "ひとこと感想",
    )
    song = models.ForeignKey(
        Song,
        verbose_name="該当曲",
        default=1,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        "コメント投稿日時",
        # default=timezone.now(),
        auto_now_add=True, #だと入力欄の表示をなしにできる。auto_nowだと更新の度に格納される
    )

    # class Meta:
    #     ordering = ('song',) # 管理画面でも効く！

    def __str__(self):
        return self.text[:64]




