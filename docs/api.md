# API エンドポイント定義

## ベース URL

Render デプロイ後のベース URL は `https://<サービス名>.onrender.com` となる。

## エンドポイント一覧

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/v1/address/{postal_code}` | 郵便番号から住所を検索 |
| GET | `/api/v1/health` | ヘルスチェック |

## リクエスト・レスポンス定義

### GET /api/v1/address/{postal_code}

郵便番号に該当する住所情報をすべて返す。

**パスパラメータ:**

| パラメータ | 型 | 説明 |
|-----------|------|------|
| postal_code | string | 郵便番号（ハイフン有無、全半角対応） |

**レスポンス（200 OK）:**

```json
[
  {
    "zipcode": "1000001",
    "prefecture": "東京都",
    "city": "千代田区",
    "town": "千代田",
    "pref_kana": "トウキョウト",
    "city_kana": "チヨダク",
    "town_kana": "チヨダ",
    "multiple_postal": 0,
    "koaza": 0,
    "chome": 0,
    "multiple_town": 0,
    "update_status": 0,
    "change_reason": 0
  }
]
```

**レスポンス（404 Not Found）:**

```json
{
  "detail": "該当する住所が見つかりません"
}
```

### GET /api/v1/health

API の稼働状態を返す。

**レスポンス（200 OK）:**

```json
{
  "status": "ok",
  "version": "0.4.2"
}
```

## エラーレスポンス定義

| ステータスコード | 説明 |
|----------------|------|
| 200 | 正常 |
| 404 | 該当する住所が見つからない |
| 422 | バリデーションエラー（FastAPI 自動生成） |
