import os
import sqlite3
import unicodedata
from typing import List, Optional

from .models import Zip2Addr


def _get_db_path() -> str:
    base = os.path.dirname(__file__)
    return os.path.join(base, "zip2addr.db")


def _normalize_postal(postal_code: str) -> str:
    # Normalize unicode, convert full-width to half-width where applicable, remove non-digits
    s = unicodedata.normalize("NFKC", postal_code)
    # keep only digits
    return "".join(ch for ch in s if ch.isdigit())


def lookup(postal_code: str, db_path: Optional[str] = None) -> List[Zip2Addr]:
    """Lookup postal code and return list of Zip2Addr (all matches).

    Args:
        postal_code: postal code string (with or without hyphen, full/half width allowed)
        db_path: optional path to sqlite DB; if omitted use bundled db
    """
    if not postal_code:
        return []
    key = _normalize_postal(postal_code)
    db = db_path or _get_db_path()
    if not os.path.exists(db):
        return []
    results: List[Zip2Addr] = []
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT zipcode, jis_code, old_postal_code, pref_kana, city_kana, town_kana, prefecture, city, town, multiple_postal, koaza, chome, multiple_town, update_status, change_reason FROM postal WHERE zipcode = ?",
            (key,),
        )
        rows = cur.fetchall()
        for r in rows:
            results.append(Zip2Addr.from_row(r))
    return results


class Zip2AddrService:
    """Service wrapper for DB path and caching."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or _get_db_path()

    def lookup(self, postal_code: str) -> List[Zip2Addr]:
        return lookup(postal_code, db_path=self.db_path)
