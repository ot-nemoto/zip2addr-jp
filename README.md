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
python3 scripts/generate_db.py utf2ken_all.csv zip2addr.db
python -c "from zip2addr import lookup; print(lookup('100-0001').to_dict())"
```

```bash
# 開発用依存を入れずにテストを回す場合
PYTHONPATH=src pytest -q

# DB を生成して動作確認する例
python3 scripts/generate_db.py utf2ken_all.csv zip2addr.db
python -c "from zip2addr import lookup; print(lookup('100-0001'))"
```

注意: CI では `PYTHONPATH=src pytest` を実行します。

## 提供している機能

- `lookup(postal_code: str) -> list[Zip2Addr]` — 郵便番号を正規化して検索し、該当するすべての `Zip2Addr` をリストで返します。見つからなければ空リストを返します。
- 同梱の `zip2addr.db`（`src/zip2addr/zip2addr.db`）は `scripts/generate_db.py` で生成できます。データは "全入れ替え" ポリシーです（既存データは DROP → 再生成します）。

## API 使い方（例）

```python
from zip2addr import lookup

# 全候補を取得（リストを返す）
all_res = lookup('100-0001')
for r in all_res:
	print(r.to_dict())
```

## CLI 使い方

- インストール済みの entry point を使う（`pyproject.toml` の `project.scripts` で `zip2addr` を定義）:

```bash
zip2addr 1000001
```

- デバッグログを出力する場合は `--debug` フラグを追加:

```bash
zip2addr 1000001 --debug
```

- インストールせずに直接実行する場合:

```bash
PYTHONPATH=src python -m zip2addr.cli 1000001
PYTHONPATH=src python -m zip2addr.cli 1000001 --debug
```

## Release からの入手とインストール

- **リリース成果物（wheel/sdist）を直接ダウンロードしてインストールする手順**:

```bash
# GitHub Releases ページに移動し、該当バージョン（例: vX.Y.Z）から
# wheel ファイル（*.whl）またはソースアーカイブ（*.tar.gz）をダウンロードします。
# 例: ダウンロードしたファイル名が zip2addr-0.1.0-py3-none-any.whl の場合
python -m pip install --upgrade pip
python -m pip install ./zip2addr-0.1.0-py3-none-any.whl

# またはソース配布を使う場合
python -m pip install ./zip2addr-0.1.0.tar.gz
```

- **インストール後の使用**:

```bash
# パッケージに同梱されたデータベースを自動で使用
zip2addr 1000001
```

## DB 生成と運用ポリシー

- `scripts/generate_db.py utf_ken_all.csv out.db` を実行すると、`out.db` を DROP → 全行挿入（サロゲート PK を持つスキーマ）で再生成します。データ更新は全入れ替えが基本です。
- 生成された DB は `zipcode` に対してインデックスを持つため、`SELECT ... WHERE zipcode = ?` は高速です。

## 開発フロー（推奨）

- 開発中は editable インストールを行うと便利:

```bash
python -m pip install -e .[test]
```

- あるいはインストールせずに環境変数で直接実行する方法:

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m zip2addr.cli 1000001
```

## バージョン管理

- バージョンは `pyproject.toml` で一元管理しています
- `src/zip2addr/__init__.py` は `importlib.metadata.version()` で `pyproject.toml` から動的に読み込みます
- **バージョン更新時は `pyproject.toml` のみを修正してください**。他ファイルへの同期は自動です。

## 注意点

-- CSV には同一郵便番号の重複行が存在します。現在の方針は「全行保持」であり、検索 API は `lookup()` が全候補を返すため、複数候補を取得できます。

- パッケージにデータを同梱する場合、リポジトリのサイズが大きくなる点に注意してください（Git LFS や Releases の利用を検討）。
