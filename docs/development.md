# 開発ガイド

## ローカルセットアップ

### Dev Container（推奨）

VS Code の Dev Container を使用する。`.devcontainer/devcontainer.json` で Python 3.12 環境が構築される。

```bash
# Dev Container 起動後、自動で以下が実行される（postCreate.sh）
sudo apt-get install -y sqlite3
pip install -e .[test]
```

### 手動セットアップ

```bash
# Python 3.9+ が必要
python -m pip install --upgrade pip
python -m pip install -e ".[test]"

# ruff（リンター）を使用する場合
python -m pip install ruff
```

## DB 操作

### データベースの再生成

日本郵便のデータから SQLite DB を生成する。

```bash
# データダウンロード
curl -sSL -o utf_ken_all.zip https://www.post.japanpost.jp/service/search/zipcode/download/utf/zip/utf_ken_all.zip
unzip -o utf_ken_all.zip

# DB 生成
python scripts/generate_db.py utf_ken_all.csv src/zip2addr/zip2addr.db
```

### DB の中身を確認

```bash
sqlite3 src/zip2addr/zip2addr.db "SELECT * FROM postal WHERE zipcode = '1000001';"
```

## テスト実行

```bash
# テスト
pytest -q

# リント
ruff check .
```

## ブランチ運用

| ブランチ | 役割 |
|---------|------|
| `develop` | デフォルトブランチ。開発・データ更新はここで行う |
| `master` | リリースブランチ。マージ時に自動でリリースが作成される |
| `feature/*`, `fix/*`, `docs/*` 等 | 作業ブランチ。develop への PR を作成する |

### フロー

1. Issue を作成
2. 作業ブランチを切って実装
3. develop へ PR → マージ
4. `auto-pr-to-master.yml` が日次で develop → master の PR を自動作成
5. 手動で master へマージ → 自動リリース

## デプロイ手順

master へのマージで GitHub Actions が自動実行される。

1. `bump-version.yml` — PR のラベル（`bump:patch` / `bump:minor`）に応じてバージョンバンプ
2. `release.yml` — wheel ビルド + GitHub Release 作成
