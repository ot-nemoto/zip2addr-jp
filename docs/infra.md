# インフラ構成

## 構成図

```
[クライアント] → [Render (Free)] → [FastAPI + uvicorn] → [SQLite DB (同梱)]
```

## 環境一覧

| 環境 | URL | 備考 |
|------|-----|------|
| 本番 | `https://<サービス名>.onrender.com` | Render Free プラン |

## Render Free プランの制限

- 0.1 vCPU / 512MB RAM
- 15 分無通信でスリープ（コールドスタートあり）
- 月 750 時間（他サービスと共有）

## デプロイ手順

### 初回セットアップ

1. [Render](https://render.com) にサインアップ
2. Dashboard → **New** → **Blueprint** を選択
3. GitHub リポジトリ `ot-nemoto/zip2addr-jp` を接続
4. `render.yaml` が自動検出され、サービスが作成される
5. デプロイが完了したら、提供される URL で API にアクセス可能

### 手動デプロイ

1. Render Dashboard → 対象サービスを選択
2. **Manual Deploy** → **Deploy latest commit** をクリック

### 自動デプロイ

Render は接続した GitHub リポジトリの master ブランチへのプッシュを検出し、自動でデプロイを実行する。
