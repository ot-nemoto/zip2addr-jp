# zip2addr-jp

日本の郵便番号から住所を高速に検索する Python ライブラリ。日本郵便の公開データを SQLite データベースとしてパッケージに同梱し、インストール後すぐに利用できます。

## 機能

- 郵便番号から住所を検索（全候補を返す）
- ハイフン・全角数字など柔軟な入力形式に対応
- CLI から JSON 形式で出力
- 外部依存なし（Python 標準ライブラリのみ）
- 月次の自動データ更新チェック

## ドキュメント

| ファイル | 内容 |
|---------|------|
| [docs/product.md](docs/product.md) | プロダクトの目的・対象ユーザー・成功指標 |
| [docs/requirements.md](docs/requirements.md) | 機能要件・非機能要件 |
| [docs/architecture.md](docs/architecture.md) | 技術スタック・ディレクトリ構成 |
| [docs/development.md](docs/development.md) | 開発セットアップ・ブランチ運用・デプロイ手順 |
| [docs/testing.md](docs/testing.md) | テスト方針・実行手順 |
| [docs/e2e-scenarios.md](docs/e2e-scenarios.md) | E2E テストシナリオ |
| [docs/tasks.md](docs/tasks.md) | タスク管理・フェーズ構成 |

## クイックスタート

```bash
# 最新版をインストール（GitHub Releases から）
pip install https://github.com/ot-nemoto/zip2addr-jp/releases/latest/download/zip2addr_jp-$(curl -s https://api.github.com/repos/ot-nemoto/zip2addr-jp/releases/latest | grep tag_name | cut -d'"' -f4 | sed 's/^v//')-py3-none-any.whl

# CLI で検索
zip2addr 1000001

# Python API
python -c "from zip2addr import lookup; print(lookup('1000001'))"
```

詳細は [docs/development.md](docs/development.md) を参照。

## ライセンス

MIT License
