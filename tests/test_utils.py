"""Unit tests for helper functions."""

from app.seed import clean_float, clean_int, clean_str


class TestCleanFloat:
    def test_valid_number(self):
        assert clean_float(25.5) == 25.5

    def test_string_number(self):
        assert clean_float("30") == 30.0

    def test_none(self):
        assert clean_float(None) is None

    def test_nan(self):
        assert clean_float(float("nan")) is None


class TestCleanInt:
    def test_valid(self):
        assert clean_int(2016) == 2016

    def test_float_to_int(self):
        assert clean_int(25.0) == 25

    def test_none(self):
        assert clean_int(None) is None


class TestCleanStr:
    def test_valid(self):
        assert clean_str("Gold") == "Gold"

    def test_none(self):
        assert clean_str(None) is None

    def test_nan(self):
        assert clean_str(float("nan")) is None
