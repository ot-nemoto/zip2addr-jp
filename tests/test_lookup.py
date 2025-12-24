import os
import sqlite3

from zip2addr import lookup


def test_lookup_basic(tmp_path):
    db = tmp_path / "test.db"
    conn = sqlite3.connect(str(db))
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE postal (zipcode TEXT PRIMARY KEY, jis_code TEXT, old_postal_code TEXT, pref_kana TEXT, city_kana TEXT, town_kana TEXT, prefecture TEXT, city TEXT, town TEXT, multiple_postal INTEGER, koaza INTEGER, chome INTEGER, multiple_town INTEGER, update_status INTEGER, change_reason INTEGER)"
    )
    cur.execute(
        "INSERT INTO postal (zipcode, jis_code, old_postal_code, pref_kana, city_kana, town_kana, prefecture, city, town) VALUES ('1000001','13101','100','ﾄｳｷｮｳﾄ','ﾁﾖﾀﾞｸ','ﾁﾖﾀﾞ','東京都','千代田区','千代田')"
    )
    conn.commit()
    conn.close()

    # monkeypatch the package db location by copying file next to package
    pkg_db = os.path.join(
        os.path.dirname(__import__("zip2addr").__file__), "zip2addr.db"
    )
    with open(db, "rb") as r, open(pkg_db, "wb") as w:
        w.write(r.read())

    res = lookup("100-0001")
    assert res is not None
    assert isinstance(res, list)
    assert len(res) == 1
    rec = res[0]
    assert rec.prefecture == "東京都"
    assert rec.city == "千代田区"
    assert rec.zipcode == "1000001"
