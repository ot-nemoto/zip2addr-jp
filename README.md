# zip2addr-jp

日本の郵便番号から住所を高速に検索する Python ライブラリ。日本郵便の公開データを使用し、パッケージに SQLite データベースを同梱しているため、インストール後すぐに利用できます。

## インストール

[GitHub Releases](https://github.com/ot-nemoto/zip2addr-jp/releases) から最新版をダウンロードしてインストールしてください。

```bash
# 例: v0.3.0 の場合
pip install https://github.com/ot-nemoto/zip2addr-jp/releases/download/v0.3.0/zip2addr_jp-0.3.0-py3-none-any.whl
```

または、リリースページから wheel ファイル（`.whl`）をダウンロードして、ローカルからインストール：

```bash
pip install ./zip2addr_jp-0.3.0-py3-none-any.whl
```

## 使い方

### Python（API）

```python
from zip2addr import lookup

# 郵便番号を検索（リストで全候補を返す）
results = lookup('100-0001')

for addr in results:
    print(f"都道府県: {addr.prefecture}")
    print(f"市区町村: {addr.city}")
    print(f"町村名: {addr.town}")
    print()

# 1件の場合は辞書に変換
if len(results) == 1:
    print(results[0].to_dict())
```

**対応する郵便番号の形式：**

- ハイフン付き：`100-0001`
- ハイフンなし：`1000001`
- 全角数字：`１００－０００１`

### コマンドライン（CLI）

```bash
# 郵便番号で住所を検索
zip2addr 1000001

# JSON 形式で出力
# {"zipcode": "1000001", "prefecture": "東京都", "city": "千代田区", "town": "千代田", ...}

# バージョン確認
zip2addr --version

# デバッグログを表示（開発時）
zip2addr 1000001 --debug
```

## 特徴

- **インストール後すぐに利用可能** — データベースはパッケージに同梱
- **複数候補に対応** — 同一郵便番号に複数の住所が存在する場合、すべて返す
- **柔軟な入力形式** — ハイフン、全角数字などの各種形式に対応
- **JSON 出力** — CLI からは JSON 形式で結果を出力
- **軽量** — 外部依存なし

## データ情報

- **データ提供元** — 日本郵便（utf_ken_all.csv）
- **更新方法** — リリース時にデータを更新します（リリースノートで確認可能）
- **データベース** — SQLite 形式（zipcode でインデックス最適化）

## API リファレンス

### `lookup(postal_code: str) -> list[Zip2Addr]`

郵便番号を検索し、該当する全ての住所候補をリストで返します。

**パラメータ：**

- `postal_code` (str) — 郵便番号（ハイフン有無、全半角を自動正規化）

**戻り値：**

- `list[Zip2Addr]` — 住所情報のリスト。見つからない場合は空リスト

**Zip2Addr オブジェクトの属性：**

- `zipcode` — 郵便番号
- `prefecture` — 都道府県
- `city` — 市区町村
- `town` — 町村名
- `pref_kana` — 都道府県（カナ）
- `city_kana` — 市区町村（カナ）
- `town_kana` — 町村名（カナ）
- その他メタデータ（`jis_code`, `old_postal_code` など）

## ライセンス

MIT License
