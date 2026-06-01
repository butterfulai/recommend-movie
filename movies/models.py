from django.db import models
from django.conf import settings


class Movie(models.Model):

    # 目的はプルダウン化
    # 使用方法は引数にchoices=GENRE_CHOICESを入れる
    GENRE_CHOICES = [
        # 選択肢の定義：（DBに保存される値, 画面に表示される名前）
        ('SF','SF')
        ,('アクション','アクション')
        ,('コメディ','コメディ')
        ,('サスペンス','サスペンス')
        ,('ドラマ','ドラマ')
        ,('ファンタジー','ファンタジー')
        ,('ホラー','ホラー')
        ,('ミステリー','ミステリー')
        ,('恋愛','恋愛')
        ,('その他','その他')
    ]

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=80,choices=GENRE_CHOICES)
    sub_genre = models.CharField(blank=True,max_length=80)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'title']

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'],
                name='unique_favorite_user_movie',
            ),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} likes {self.movie}'
