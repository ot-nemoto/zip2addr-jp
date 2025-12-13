# zip2addr-jp

軽量な郵便番号 → 住所検索の Python ライブラリ（プロトタイプ）。日本郵便の `utf_ken_all.csv` を SQLite に変換して検索します。

## 主なファイル

- `src/zip2addr` — ライブラリ本体 (`api.py`, `models.py`)
- `scripts/generate_db.py` — CSV から SQLite DB (`postal` テーブル) を生成するスクリプト
- `tests/` — テスト一式（`conftest.py` により `src/` を自動でパスに追加します）
- `.github/workflows/ci.yml` — CI (pytest)

## クイックスタート

1. 小さなテストを実行する（開発環境）:

```bash
pytest -q
```

2. 実データから DB を生成して動作確認する:

```bash
python3 scripts/generate_db.py utf_ken_all.csv zip2addr.db
python -c "from zip2addr.api import lookup; print(lookup('100-0001').to_dict())"
```

```bash
# 開発用依存を入れずにテストを回す場合
PYTHONPATH=src pytest -q

# DB を生成して動作確認する例
python3 scripts/generate_db.py utf_ken_all.csv zip2addr.db
python -c "from zip2addr.api import lookup; print(lookup('100-0001'))"
```

注意: CI では `PYTHONPATH=src pytest` を実行します。
