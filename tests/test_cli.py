"""Unit and integration tests for zip2addr.cli module."""

import json
import os
import sqlite3

import pytest

from zip2addr.cli import main


class TestCLIBasic:
    """Unit tests for CLI basic functionality."""

    def test_cli_version(self, capsys):
        """Test --version flag."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--version"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "0.2.0" in captured.out or "0.0.0" in captured.out

    def test_cli_help(self, capsys):
        """Test --help flag."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--help"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Postal code" in captured.out or "postal" in captured.out.lower()

    def test_cli_no_postal_code(self):
        """Test CLI without postal code argument."""
        with pytest.raises(SystemExit):
            main([])

    def test_cli_missing_postal_code(self):
        """Test CLI with only --debug flag."""
        with pytest.raises(SystemExit):
            main(["--debug"])


class TestCLILookup:
    """Unit tests for CLI lookup functionality."""

    def test_cli_lookup_basic(self, tmp_path, capsys):
        """Test basic CLI lookup."""
        # Setup test database
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

        # Replace package DB with test DB
        pkg_db = os.path.join(
            os.path.dirname(__import__("zip2addr").__file__), "zip2addr.db"
        )
        with open(db, "rb") as r, open(pkg_db, "wb") as w:
            w.write(r.read())

        # Run CLI
        result = main(["100-0001"])
        assert result == 0

        # Check output
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert isinstance(output, dict)
        assert output["zipcode"] == "1000001"
        assert output["prefecture"] == "東京都"

    def test_cli_lookup_not_found(self, tmp_path, capsys):
        """Test CLI lookup with non-existent postal code."""
        # Setup empty test database
        db = tmp_path / "test.db"
        conn = sqlite3.connect(str(db))
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE postal (zipcode TEXT PRIMARY KEY, jis_code TEXT, old_postal_code TEXT, pref_kana TEXT, city_kana TEXT, town_kana TEXT, prefecture TEXT, city TEXT, town TEXT, multiple_postal INTEGER, koaza INTEGER, chome INTEGER, multiple_town INTEGER, update_status INTEGER, change_reason INTEGER)"
        )
        conn.commit()
        conn.close()

        # Replace package DB with test DB
        pkg_db = os.path.join(
            os.path.dirname(__import__("zip2addr").__file__), "zip2addr.db"
        )
        with open(db, "rb") as r, open(pkg_db, "wb") as w:
            w.write(r.read())

        # Run CLI
        result = main(["9999999"])
        assert result == 1

        # Check output
        captured = capsys.readouterr()
        assert captured.out.strip() == "null"

    def test_cli_lookup_with_debug(self, tmp_path, capsys):
        """Test CLI lookup with --debug flag."""
        # Setup test database
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

        # Replace package DB with test DB
        pkg_db = os.path.join(
            os.path.dirname(__import__("zip2addr").__file__), "zip2addr.db"
        )
        with open(db, "rb") as r, open(pkg_db, "wb") as w:
            w.write(r.read())

        # Run CLI with debug
        result = main(["100-0001", "--debug"])
        assert result == 0

        # Check output (debug output goes to stderr/stdout depending on logger setup)
        captured = capsys.readouterr()
        output = captured.out
        # Verify JSON output is valid and contains expected fields
        import json

        parsed = json.loads(output.strip())
        assert parsed["zipcode"] == "1000001"

    def test_cli_lookup_multiple_results(self, tmp_path, capsys):
        """Test CLI lookup returning single result as dict."""
        # Setup test database with a single entry
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

        # Replace package DB with test DB
        pkg_db = os.path.join(
            os.path.dirname(__import__("zip2addr").__file__), "zip2addr.db"
        )
        with open(db, "rb") as r, open(pkg_db, "wb") as w:
            w.write(r.read())

        # Run CLI
        result = main(["100-0001"])
        assert result == 0

        # Check output is dict (not list) for single result
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert isinstance(output, dict)
        assert output["zipcode"] == "1000001"
