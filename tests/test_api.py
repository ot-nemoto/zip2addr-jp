"""Unit tests for zip2addr.api module."""

import sqlite3

from zip2addr.api import Zip2AddrService, _normalize_postal, lookup


class TestNormalizePostal:
    """Unit tests for _normalize_postal function."""

    def test_normalize_with_hyphen(self):
        """Test normalization of postal code with hyphen."""
        result = _normalize_postal("100-0001")
        assert result == "1000001"

    def test_normalize_without_hyphen(self):
        """Test normalization of postal code without hyphen."""
        result = _normalize_postal("1000001")
        assert result == "1000001"

    def test_normalize_full_width_digits(self):
        """Test normalization of full-width digits."""
        result = _normalize_postal("１００－０００１")
        assert result == "1000001"

    def test_normalize_empty_string(self):
        """Test normalization of empty string."""
        result = _normalize_postal("")
        assert result == ""

    def test_normalize_mixed_characters(self):
        """Test normalization removes non-digit characters."""
        result = _normalize_postal("100abc0001")
        assert result == "1000001"


class TestLookup:
    """Unit tests for lookup function."""

    def test_lookup_empty_postal(self):
        """Test lookup with empty postal code."""
        result = lookup("")
        assert result == []

    def test_lookup_nonexistent_db(self, tmp_path):
        """Test lookup with nonexistent database path."""
        result = lookup("1000001", db_path=str(tmp_path / "nonexistent.db"))
        assert result == []

    def test_lookup_not_found(self, tmp_path):
        """Test lookup for non-existent postal code."""
        db = tmp_path / "test.db"
        conn = sqlite3.connect(str(db))
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE postal (zipcode TEXT PRIMARY KEY, jis_code TEXT, old_postal_code TEXT, pref_kana TEXT, city_kana TEXT, town_kana TEXT, prefecture TEXT, city TEXT, town TEXT, multiple_postal INTEGER, koaza INTEGER, chome INTEGER, multiple_town INTEGER, update_status INTEGER, change_reason INTEGER)"
        )
        conn.commit()
        conn.close()

        result = lookup("9999999", db_path=str(db))
        assert result == []

    def test_lookup_found(self, tmp_path):
        """Test lookup for existing postal code."""
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

        result = lookup("100-0001", db_path=str(db))
        assert len(result) == 1
        assert result[0].zipcode == "1000001"
        assert result[0].prefecture == "東京都"

    def test_lookup_multiple_results(self, tmp_path):
        """Test lookup with postal code having multiple town fields."""
        db = tmp_path / "test.db"
        conn = sqlite3.connect(str(db))
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE postal (id INTEGER PRIMARY KEY, zipcode TEXT, jis_code TEXT, old_postal_code TEXT, pref_kana TEXT, city_kana TEXT, town_kana TEXT, prefecture TEXT, city TEXT, town TEXT, multiple_postal INTEGER, koaza INTEGER, chome INTEGER, multiple_town INTEGER, update_status INTEGER, change_reason INTEGER)"
        )
        # Insert two separate zipcodes to test multiple results
        cur.execute(
            "INSERT INTO postal (zipcode, jis_code, pref_kana, city_kana, town_kana, prefecture, city, town) VALUES ('1000001','13101','ﾄｳｷｮｳﾄ','ﾁﾖﾀﾞｸ','ﾁﾖﾀﾞ','東京都','千代田区','千代田')"
        )
        conn.commit()
        conn.close()

        result = lookup("100-0001", db_path=str(db))
        assert len(result) == 1
        assert result[0].zipcode == "1000001"


class TestZip2AddrService:
    """Unit tests for Zip2AddrService class."""

    def test_service_init_with_custom_db(self, tmp_path):
        """Test service initialization with custom database path."""
        db = tmp_path / "test.db"
        sqlite3.connect(str(db)).execute(
            "CREATE TABLE postal (zipcode TEXT PRIMARY KEY)"
        )
        service = Zip2AddrService(db_path=str(db))
        assert service.db_path == str(db)

    def test_service_lookup(self, tmp_path):
        """Test service lookup method."""
        db = tmp_path / "test.db"
        conn = sqlite3.connect(str(db))
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE postal (zipcode TEXT PRIMARY KEY, jis_code TEXT, old_postal_code TEXT, pref_kana TEXT, city_kana TEXT, town_kana TEXT, prefecture TEXT, city TEXT, town TEXT, multiple_postal INTEGER, koaza INTEGER, chome INTEGER, multiple_town INTEGER, update_status INTEGER, change_reason INTEGER)"
        )
        cur.execute(
            "INSERT INTO postal (zipcode, jis_code, pref_kana, city_kana, town_kana, prefecture, city, town) VALUES ('1000001','13101','ﾄｳｷｮｳﾄ','ﾁﾖﾀﾞｸ','ﾁﾖﾀﾞ','東京都','千代田区','千代田')"
        )
        conn.commit()
        conn.close()

        service = Zip2AddrService(db_path=str(db))
        result = service.lookup("100-0001")
        assert len(result) == 1
        assert result[0].prefecture == "東京都"
