# Django DX Automation

認証済みユーザーが CSV ファイルでモデルデータのインポート／エクスポートを行える、バックグラウンド処理やメール通知付きの Django ベース自動化ツールです。Tailwind CSS で UI を構築しています。

---

## 🚀 主な機能

### ✅ ユーザー認証

- **登録 / ログイン / ログアウト**機能を Django の認証システム（`django.contrib.auth`）で実装。

### ✅ CSV データのインポート (Upload + DB保存)

- CSV ファイルをアップロードし、指定したモデルにデータをインポート。
- CSV ヘッダをモデルフィールドと照合してバリデーション。
- 成功時は **バックグラウンドで Celery タスク**を実行し、完了通知をメール送信。

### ✅ CSV データのエクスポート

- 任意モデルの全データを CSV に出力し、サーバ側 `media/exported_data/` に保存。
- **Celery タスク**でバックグラウンド処理し、完了時にメールで通知。

### ✅ Tailwind ベースの UI

- `django-tailwind` + `crispy-tailwind` でモダンな UI を構築。
- ビルド/監視には `python manage.py tailwind start` を使用。

### ✅ 開発用ホットリロード

- `django-browser-reload` を DEBUG モード時に有効化し、テンプレートや静的ファイル変更時に自動リロード。

---

## 🧩 使用している Django の主要技術 (概要)

### 🔐 認証

- `django.contrib.auth`: 認証 / セッション管理 / パスワードハッシュ。
- `AuthenticationForm` と `UserCreationForm` ベースのカスタムフォーム（`dx_automation_main/forms.py`）で、登録・ログインを実装。
- `user.is_authenticated` ビルトイン属性でアクセス制御を実装し、未認証ユーザーの不正アクセスを防止。

### �📦 アプリ構造

- `dataentry`: CSV のインポート/エクスポート機能、バックグラウンドタスク呼び出し。
- `uploads`: アップロードファイル管理用モデル (`Upload`) を保持。
- `theme`: `django-tailwind` で Tailwind CSS を管理・ビルド。

### ⚙️ バックグラウンド処理 (Celery)

- `dx_automation_main/celery.py` で Celery アプリを初期化。
- Redis をメッセージブローカー（`CELERY_BROKER_URL` / `BROKER_URL`）として利用。
- `dataentry.tasks` 内に Celery タスク (`import_data_task`, `export_data_task`) を定義。
- タスクは `django.core.management.call_command()` で management command を実行。

### 📧 メール通知

- `django.core.mail.EmailMessage` で送信。
- 設定は環境変数（`EMAIL_HOST`, `EMAIL_HOST_USER` 等）で管理。

### 🪪 管理コマンド (management/commands)

- `importdata`: 与えられた CSV を読み込み、モデルにデータを投入。
- `exportdata`: モデルから全データを CSV に出力。
- これらのコマンドは `dataentry/management/commands/` 内に定義されており、ビューや Celery タスクから `call_command()` で起動される。

### 🎨 Tailwind + Crispy Forms

- `tailwind` / `crispy_tailwind` を利用し、フォームや UI を Tailwind 準拠でレンダリング。

---

## ✅ 開発時の起動手順（例）

1. 仮想環境を有効化

   ```bash
   source env/Scripts/activate
   ```

2. 依存関係をインストール（必要に応じて）

   ```bash
   pip install -r requirements.txt
   ```

3. マイグレーション

   ```bash
   python manage.py migrate
   ```

4. Celery ワーカーを起動（Redis が必要）

   ```bash
   celery -A dx_automation_main worker --loglevel=info
   ```

5. Tailwind の開発モードを起動

   ```bash
   python manage.py tailwind start
   ```

6. Django 開発サーバを起動
   ```bash
   python manage.py runserver
   ```

---

## 🔧 必要な環境変数

- `SECRET_KEY`
- `DEBUG` (bool)
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`
- `DEFAULT_TO_EMAIL`

---

## 📂 データ保存先

- メディアファイル: `media/` (`MEDIA_ROOT`)
- エクスポート CSV: `media/exported_data/`

---

## 🎯 追加改善アイデア

- インポート時の重複チェックや更新オプション
- インポート/エクスポート処理の進捗通知（WebSocket / Django Channels）
- アップロードファイル暗号化・マルチテナント対応
