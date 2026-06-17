# アーキテクチャ

## 技術スタック

| 項目 | 技術 |
|------|------|
| 言語 | Python 3.9+ |
| データベース | SQLite（パッケージ同梱） |
| ビルド | setuptools + wheel |
| テスト | pytest |
| リンター | ruff |
| CI/CD | GitHub Actions |

## ディレクトリ構成

```
zip2addr-jp/
├── .devcontainer/          # Dev Container 設定
│   ├── devcontainer.json
│   └── postCreate.sh
├── .github/workflows/      # GitHub Actions ワークフロー
│   ├── ci.yml              # PR 時の CI（lint + test）
│   ├── data-check.yml      # 月次データ更新チェック
│   ├── auto-pr-to-master.yml  # develop → master 自動 PR
│   ├── bump-version.yml    # バージョン自動バンプ
│   └── release.yml         # master push 時のリリース作成
├── docs/                   # ドキュメント
├── scripts/
│   └── generate_db.py      # CSV → SQLite 変換スクリプト
├── src/zip2addr/           # パッケージソース
│   ├── __init__.py         # パッケージ初期化、lookup と Zip2Addr を再エクスポート
│   ├── api.py              # 検索ロジック（lookup 関数、Zip2AddrService クラス）
│   ├── cli.py              # CLI エントリーポイント
│   ├── models.py           # Zip2Addr データクラス
│   └── zip2addr.db         # 同梱 SQLite データベース（CI で生成・コミット）
├── tests/                  # テスト
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_cli.py
│   └── test_models.py
├── CLAUDE.md               # Claude Code 作業ルール
├── pyproject.toml          # プロジェクト設定・依存管理
└── README.md
```

## 環境変数

特になし。すべての設定はコード内で完結する。

## データフロー

1. 日本郵便が `utf_ken_all.csv` を公開（月次更新）
2. `data-check.yml` が月次でダウンロード・チェックサム比較
3. 変更があれば `scripts/generate_db.py` で SQLite DB を再生成し develop にコミット
4. `auto-pr-to-master.yml` が日次で develop → master の PR を自動作成
5. 手動マージ後、`bump-version.yml` がバージョンバンプ
6. `release.yml` が wheel をビルドし GitHub Release を作成

## バージョン固有仕様・既知事項

- `importlib.resources` を使用してパッケージ内の DB ファイルを参照（wheel 内の zip 展開にも対応）
