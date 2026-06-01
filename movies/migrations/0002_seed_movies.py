from django.db import migrations


MOVIES = [
    {
        'title': '星屑の航路',
        'genre': 'SF',
        'description': '辺境惑星へ向かう調査船の乗組員が、未知の信号に導かれて自分たちの記憶と向き合うSFドラマ。',
        'image_url': 'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=1200&q=80',
    },
    {
        'title': '雨上がりの約束',
        'genre': '恋愛',
        'description': '小さな港町で再会した幼なじみが、過去のすれ違いをほどきながら未来を選び直すラブストーリー。',
        'image_url': 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80',
    },
    {
        'title': 'ラスト・チェイス',
        'genre': 'アクション',
        'description': '元刑事と若きハッカーが、巨大企業の陰謀を暴くため夜の都市を駆け抜けるクライムアクション。',
        'image_url': 'https://images.unsplash.com/photo-1493246507139-91e8fad9978e?auto=format&fit=crop&w=1200&q=80',
    },
    {
        'title': 'ミッドナイト・キッチン',
        'genre': 'コメディ',
        'description': '深夜食堂を舞台に、常連客たちの珍騒動と人生の小さな転機を描く群像コメディ。',
        'image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80',
    },
    {
        'title': '透明な境界線',
        'genre': 'ドラマ',
        'description': '地方都市の高校教師が、生徒たちとの交流を通じて失った情熱を取り戻していくヒューマンドラマ。',
        'image_url': 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=1200&q=80',
    },
    {
        'title': '古城の暗号',
        'genre': 'ミステリー',
        'description': 'ヨーロッパの古城に残された暗号をめぐり、歴史学者と探偵が隠された真実に迫るミステリー。',
        'image_url': 'https://images.unsplash.com/photo-1520637836862-4d197d17c90a?auto=format&fit=crop&w=1200&q=80',
    },
]


def create_movies(apps, schema_editor):
    movie = apps.get_model('movies', 'Movie')
    for item in MOVIES:
        movie.objects.get_or_create(title=item['title'], defaults=item)


def remove_movies(apps, schema_editor):
    movie = apps.get_model('movies', 'Movie')
    movie.objects.filter(title__in=[item['title'] for item in MOVIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_movies, remove_movies),
    ]
