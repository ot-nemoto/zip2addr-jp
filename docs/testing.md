# テスト方針

## テスト種別

| 種別 | 対象 | ツール |
|------|------|--------|
| ユニットテスト | API（`lookup`）、モデル（`Zip2Addr`）、CLI | pytest |
| リント | コード全体 | ruff |

## テストファイル構成

```
tests/
├── conftest.py       # 共通フィクスチャ
├── test_api.py       # lookup 関数のテスト
├── test_cli.py       # CLI のテスト
└── test_models.py    # Zip2Addr モデルのテスト
```

## 完了条件

- API（`lookup` 関数、`Zip2AddrService`）のユニットテストが通ること
- CLI のユニットテストが通ること
- `ruff check .` でリントエラーがないこと

## カバレッジ方針

- `src/zip2addr/api.py` と `src/zip2addr/cli.py` の主要パスをカバーする
- 正常系・異常系（空入力、存在しない郵便番号）をテストする

## 実行手順

```bash
# テスト実行
pytest -q

# 詳細出力
pytest -v

# リント
ruff check .
```
