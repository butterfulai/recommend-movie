# 映画レコメンドシステム

Django で作った、映画のおすすめアプリです。

ユーザーが映画を「お気に入り」すると、その情報をもとにおすすめ映画を表示します。
たとえば、自分と同じ映画をお気に入りしている人が、別の映画もお気に入りしていた場合、その映画が「あなたへのおすすめ」として出ます。

## このアプリでできること

- 映画一覧を見る
- 映画の詳細を見る
- メールアドレスとパスワードで新規登録する
- メールアドレスとパスワードでログインする
- Googleアカウントでログインする
- ログイン後、映画をお気に入り登録・解除する
- マイページで自分のお気に入り映画を見る
- マイページで自分向けのおすすめ映画を見る

## 使っている技術

- Python
- Django 5.2
- SQLite / PostgreSQL
- django-allauth
- Bootstrap 5

開発中は SQLite でも動きます。
PostgreSQL を使いたい場合は、環境変数を設定すると PostgreSQL に切り替わります。

## フォルダ構成

```text
recommend_movie/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── movie_recommend/
│   ├── settings.py
│   └── urls.py
├── movies/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── recommendations.py
│   ├── tests.py
│   └── migrations/
└── templates/
    ├── base.html
    ├── account/
    │   ├── login.html
    │   └── signup.html
    └── movies/
        ├── home.html
        ├── mypage.html
        ├── detail.html
        └── _movie_grid.html
```

## 重要なファイル

### `movies/models.py`

データベースの形を決めているファイルです。

このアプリでは主に2つのデータがあります。

### `Movie`

映画データです。

- タイトル
- ジャンル
- 説明文
- 画像URL

を持っています。

### `Favorite`

お気に入りデータです。

「誰が」「どの映画を」お気に入りしたかを保存します。

同じユーザーが同じ映画を2回お気に入りできないように、重複防止の設定も入っています。

## レコメンドの仕組み

レコメンド処理は `movies/recommendations.py` にあります。

使っているのは、簡易的な協調フィルタリングです。

難しく言うと「ユーザーベース協調フィルタリング」です。
簡単に言うと、こういう考え方です。

1. 自分がお気に入りした映画を調べる
2. その映画を同じようにお気に入りしている他のユーザーを探す
3. その人たちが他にお気に入りしている映画を探す
4. 自分がまだお気に入りしていない映画だけを残す
5. 多くの類似ユーザーに選ばれている映画を上位に表示する

例:

```text
自分: A映画が好き
田中さん: A映画とB映画が好き
佐藤さん: A映画とB映画とC映画が好き

この場合、自分にはB映画やC映画がおすすめされやすくなります。
```

機械学習ライブラリは使わず、Django ORM で実装しています。
そのため、ポートフォリオとして説明しやすい作りになっています。

## 画面URL

| URL | 内容 |
| --- | --- |
| `/` | トップページ |
| `/accounts/login/` | ログイン |
| `/accounts/signup/` | 新規登録 |
| `/mypage/` | マイページ |
| `/movies/1/` | 映画詳細ページ |

## 起動方法

このプロジェクトでは `.venv` という仮想環境を使っています。

cmd でプロジェクトフォルダに移動します。

```cmd
cd C:\Users\GuestUser\Desktop\dev\recommend_movie
```

仮想環境に入ります。

```cmd
conda activate C:\Users\GuestUser\Desktop\dev\recommend_movie\.venv
```

もし `conda activate` がうまくいかない場合は、仮想環境に入らずに直接実行しても大丈夫です。

```cmd
.venv\python.exe manage.py runserver
```

仮想環境に入れた場合は、次のコマンドで起動できます。

```cmd
python manage.py runserver
```

起動したら、ブラウザでここを開きます。

```text
http://127.0.0.1:8000/
```

## データベースを準備する

初回だけ、またはモデルを変更した後はマイグレーションを実行します。

```cmd
python manage.py migrate
```

仮想環境に入らず直接実行する場合はこちらです。

```cmd
.venv\python.exe manage.py migrate
```

## 管理者ユーザーを作る

管理画面を使いたい場合は、管理者ユーザーを作ります。

```cmd
python manage.py createsuperuser
```

管理画面はこちらです。

```text
http://127.0.0.1:8000/admin/
```

## メールアドレス登録・ログイン

このアプリでは、メールアドレスとパスワードだけで登録できます。

登録ページ:

```text
http://127.0.0.1:8000/accounts/signup/
```

ログインページ:

```text
http://127.0.0.1:8000/accounts/login/
```

メールアドレスはユニークです。
つまり、同じメールアドレスで2つのアカウントは作れません。

## Googleログインを使う場合

Googleログインを使うには、Google Cloud Console で OAuth クライアントIDとクライアントシークレットを作る必要があります。

このプロジェクトでは、IDやシークレットを `settings.py` に直接書かず、環境変数から読み込むようにしています。

cmd でサーバーを起動する前に、次のように設定します。

```cmd
set GOOGLE_OAUTH_CLIENT_ID=ここにクライアントID
set GOOGLE_OAUTH_CLIENT_SECRET=ここにクライアントシークレット
python manage.py runserver
```

Google Cloud Console 側には、リダイレクトURIとして次を登録します。

```text
http://127.0.0.1:8000/accounts/google/login/callback/
```

`localhost` でアクセスする場合は、こちらも登録します。

```text
http://localhost:8000/accounts/google/login/callback/
```

## PostgreSQL を使う場合

何も設定しない場合、このアプリは SQLite を使います。

PostgreSQL を使う場合は、cmd で次の環境変数を設定してから起動します。

```cmd
set DB_ENGINE=postgresql
set POSTGRES_DB=movie_recommend
set POSTGRES_USER=postgres
set POSTGRES_PASSWORD=your_password
set POSTGRES_HOST=localhost
set POSTGRES_PORT=5432
python manage.py migrate
python manage.py runserver
```

`your_password` は、自分の PostgreSQL のパスワードに置き換えてください。

## テストの実行

このアプリには、レコメンドやログインまわりの簡単なテストがあります。

```cmd
python manage.py test
```

仮想環境に入らず直接実行する場合はこちらです。

```cmd
.venv\python.exe manage.py test
```

## よくあるエラー

### `Missing required parameter: client_id`

Googleログイン用のクライアントIDが設定されていない時に出ます。

cmd で次を設定してから、サーバーを再起動してください。

```cmd
set GOOGLE_OAUTH_CLIENT_ID=ここにクライアントID
set GOOGLE_OAUTH_CLIENT_SECRET=ここにクライアントシークレット
python manage.py runserver
```

### `redirect_uri_mismatch`

Google Cloud Console に登録したリダイレクトURIと、実際に使っているURLが違う時に出ます。

`127.0.0.1` で開いているなら、これを登録します。

```text
http://127.0.0.1:8000/accounts/google/login/callback/
```

`localhost` で開いているなら、これを登録します。

```text
http://localhost:8000/accounts/google/login/callback/
```

### `conda activate` が使えない

仮想環境に入れなくても、次のように直接実行できます。

```cmd
.venv\python.exe manage.py runserver
```

## 開発メモ

このアプリは、まず分かりやすさを優先して作っています。

本格的に育てるなら、次のような機能を追加できます。

- 映画検索
- ジャンル絞り込み
- 評価点数
- レビュー投稿
- お気に入り数ランキングの強化
- レコメンド精度の改善
- PostgreSQL 前提の本番環境化

## 追加・変更した機能

- `Movie` モデルの `genre`（ジャンル）フィールドは、もともと80文字以内で自由に入力できる形式でした。
  今回は、プルダウンから選択できるように変更しました。選択肢は以下のとおりです。

```
[アクション, サスペンス, ホラー, SF, ファンタジー, コメディ, 恋愛, ドラマ, ミステリー, その他]
```

- 映画のジャンルは必ずしも1つに決まるわけではないため、補足用の `sub_genre` フィールドも追加しました。
  `sub_genre` は空欄も許可しており、80文字以内で自由に入力できます。

## 開発における生成AIの活用

本アプリの開発では、生産性向上のため生成AI（Gemini、Codex）を活用しました。

- Codexに伝える仕様書をまとめるために、Geminiを活用しました。
- Codexに仕様書を伝え、アプリ全体の初期コードを作成しました。

**【こだわり】**

AIが生成したコードをそのまま使用するだけではなく、使用している関数や機能、設定ファイルなどについて
AIに解説を求め、内容を理解したうえでコードを使用しています。
また、「追加・変更した機能」に記載した内容は、生成AIを使わずに自分で実装しました。
