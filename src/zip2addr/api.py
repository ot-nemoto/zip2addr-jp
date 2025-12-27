import importlib.resources
import logging
import os
import sqlite3
import unicodedata
from typing import List, Optional

from .models import Zip2Addr

logger = logging.getLogger(__name__)


def _get_db_path() -> str:
    # Use importlib.resources to locate the bundled DB safely even when
    # installed from a wheel (which may store package data in zip files).
    db_resource = importlib.resources.files("zip2addr").joinpath("zip2addr.db")
    # as_file will extract to a temporary file if necessary and yield a path
    with importlib.resources.as_file(db_resource) as p:
        return str(p)


def _normalize_postal(postal_code: str) -> str:
    # Normalize unicode, convert full-width to half-width where applicable, remove non-digits
    s = unicodedata.normalize("NFKC", postal_code)
    # keep only digits
    normalized = "".join(ch for ch in s if ch.isdigit())
    logger.debug(f"Normalized postal code: {postal_code} -> {normalized}")
    return normalized


def lookup(postal_code: str, db_path: Optional[str] = None) -> List[Zip2Addr]:
    """Lookup postal code and return list of Zip2Addr (all matches).

    Args:
        postal_code: postal code string (with or without hyphen, full/half width allowed)
        db_path: optional path to sqlite DB; if omitted use bundled db
    """
    logger.debug(f"Looking up postal code: {postal_code}")
    if not postal_code:
        logger.debug("Empty postal code provided")
        return []
    key = _normalize_postal(postal_code)
    db = db_path or _get_db_path()
    logger.debug(f"Using database: {db}")
    if not os.path.exists(db):
        logger.debug(f"Database file not found: {db}")
        return []
    results: List[Zip2Addr] = []
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        logger.debug(f"Querying database for zipcode: {key}")
        cur.execute(
            "SELECT zipcode, jis_code, old_postal_code, pref_kana, city_kana, town_kana, prefecture, city, town, multiple_postal, koaza, chome, multiple_town, update_status, change_reason FROM postal WHERE zipcode = ?",
            (key,),
        )
        rows = cur.fetchall()
        logger.debug(f"Found {len(rows)} result(s)")
        for r in rows:
            results.append(Zip2Addr.from_row(r))
    return results


class Zip2AddrService:
    """Service wrapper for DB path and caching."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or _get_db_path()
        logger.debug(f"Initialized Zip2AddrService with db_path: {self.db_path}")

    def lookup(self, postal_code: str) -> List[Zip2Addr]:
        logger.debug(f"Service lookup called for: {postal_code}")
        return lookup(postal_code, db_path=self.db_path)
