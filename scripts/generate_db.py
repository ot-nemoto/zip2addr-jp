#!/usr/bin/env python3
"""Generate sqlite DB from utf_ken_all.csv (minimal implementation).

Usage: python scripts/generate_db.py utf_ken_all.csv out.db
"""

import csv
import sqlite3
import sys


def create_db(csv_path: str, out_db: str):
    # Recreate DB from scratch to ensure full replace semantics
    conn = sqlite3.connect(out_db)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS postal")
    cur.execute(
        """
        CREATE TABLE postal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zipcode TEXT,
            jis_code TEXT,
            old_postal_code TEXT,
            pref_kana TEXT,
            city_kana TEXT,
            town_kana TEXT,
            prefecture TEXT,
            city TEXT,
            town TEXT,
            multiple_postal INTEGER,
            koaza INTEGER,
            chome INTEGER,
            multiple_town INTEGER,
            update_status INTEGER,
            change_reason INTEGER
        )
        """
    )
    # create index on zipcode for fast lookup
    cur.execute("CREATE INDEX IF NOT EXISTS idx_postal_zipcode ON postal(zipcode)")
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        for row in reader:
            # Japan Post CSV columns (1-based): 1=jis,2=old5,3=zip7,4=pref_kana,5=city_kana,6=town_kana,7=pref,8=city,9=town,10=multi_postal,11=koaza,12=chome,13=multi_town,14=update_status,15=change_reason
            if len(row) < 3:
                continue
            postal = row[2].strip().replace("-", "")

            def val(i):
                return row[i].strip() if i < len(row) else ""

            jis = val(0)
            old5 = val(1)
            pref_kana = val(3)
            city_kana = val(4)
            town_kana = val(5)
            pref = val(6)
            city = val(7)
            town = val(8)
            multi_postal = int(val(9)) if val(9).isdigit() else None
            koaza = int(val(10)) if val(10).isdigit() else None
            chome = int(val(11)) if val(11).isdigit() else None
            multi_town = int(val(12)) if val(12).isdigit() else None
            update_status = int(val(13)) if val(13).isdigit() else None
            change_reason = int(val(14)) if val(14).isdigit() else None

            cur.execute(
                "INSERT INTO postal(zipcode, jis_code, old_postal_code, pref_kana, city_kana, town_kana, prefecture, city, town, multiple_postal, koaza, chome, multiple_town, update_status, change_reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    postal,
                    jis,
                    old5,
                    pref_kana,
                    city_kana,
                    town_kana,
                    pref,
                    city,
                    town,
                    multi_postal,
                    koaza,
                    chome,
                    multi_town,
                    update_status,
                    change_reason,
                ),
            )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: generate_db.py input.csv out.db")
        sys.exit(2)
    create_db(sys.argv[1], sys.argv[2])
