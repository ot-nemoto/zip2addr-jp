"""Unit tests for zip2addr.models module."""

from zip2addr.models import Zip2Addr


class TestZip2AddrModel:
    """Unit tests for Zip2Addr dataclass."""

    def test_zip2addr_creation(self):
        """Test Zip2Addr object creation."""
        addr = Zip2Addr(
            zipcode="1000001",
            prefecture="東京都",
            city="千代田区",
            town="千代田",
        )
        assert addr.zipcode == "1000001"
        assert addr.prefecture == "東京都"
        assert addr.city == "千代田区"
        assert addr.town == "千代田"

    def test_zip2addr_from_row(self):
        """Test Zip2Addr.from_row class method."""
        row = (
            "1000001",  # zipcode
            "13101",  # jis_code
            "100",  # old_postal_code
            "ﾄｳｷｮｳﾄ",  # pref_kana
            "ﾁﾖﾀﾞｸ",  # city_kana
            "ﾁﾖﾀﾞ",  # town_kana
            "東京都",  # prefecture
            "千代田区",  # city
            "千代田",  # town
            None,  # multiple_postal
            None,  # koaza
            None,  # chome
            None,  # multiple_town
            0,  # update_status
            0,  # change_reason
        )
        addr = Zip2Addr.from_row(row)
        assert addr.zipcode == "1000001"
        assert addr.prefecture == "東京都"
        assert addr.city == "千代田区"
        assert addr.town == "千代田"

    def test_zip2addr_to_dict(self):
        """Test Zip2Addr.to_dict method."""
        addr = Zip2Addr(
            zipcode="1000001",
            pref_kana="ﾄｳｷｮｳﾄ",
            city_kana="ﾁﾖﾀﾞｸ",
            town_kana="ﾁﾖﾀﾞ",
            prefecture="東京都",
            city="千代田区",
            town="千代田",
        )
        result = addr.to_dict()
        assert isinstance(result, dict)
        assert result["zipcode"] == "1000001"
        assert result["prefecture"] == "東京都"
        assert result["city"] == "千代田区"
        assert result["town"] == "千代田"

    def test_zip2addr_partial_data(self):
        """Test Zip2Addr with partial data (only required field)."""
        addr = Zip2Addr(zipcode="1000001")
        assert addr.zipcode == "1000001"
        assert addr.prefecture is None
        assert addr.city is None

    def test_zip2addr_to_dict_with_none_values(self):
        """Test Zip2Addr.to_dict with None values."""
        addr = Zip2Addr(
            zipcode="1000001",
            prefecture=None,
            city=None,
            town=None,
        )
        result = addr.to_dict()
        assert result["zipcode"] == "1000001"
        assert result["prefecture"] is None
        assert result["city"] is None

    def test_zip2addr_from_row_with_string_integers(self):
        """Test Zip2Addr.from_row handling string integers."""
        row = (
            "1000001",  # zipcode
            "13101",  # jis_code
            "100",  # old_postal_code
            "ﾄｳｷｮｳﾄ",  # pref_kana
            "ﾁﾖﾀﾞｸ",  # city_kana
            "ﾁﾖﾀﾞ",  # town_kana
            "東京都",  # prefecture
            "千代田区",  # city
            "千代田",  # town
            "1",  # multiple_postal (as string)
            "2",  # koaza (as string)
            "3",  # chome (as string)
            "0",  # multiple_town (as string)
            "1",  # update_status (as string)
            "0",  # change_reason (as string)
        )
        addr = Zip2Addr.from_row(row)
        assert addr.multiple_postal == 1
        assert addr.koaza == 2
        assert addr.chome == 3
        assert addr.update_status == 1
        assert addr.change_reason == 0
