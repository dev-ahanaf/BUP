"""Unit tests for time parsing and normalization."""
import pytest
from app.utils.time_parser import (
    extract_hour_range_from_text,
    normalize_hour_to_24,
    parse_hour_token,
    validate_and_normalize_hours,
)


def test_normalize_hour_to_24():
    assert normalize_hour_to_24(12, "PM") == 12
    assert normalize_hour_to_24(12, "AM") == 0
    assert normalize_hour_to_24(1, "PM") == 13
    assert normalize_hour_to_24(11, "PM") == 23
    assert normalize_hour_to_24(9, "AM") == 9


def test_parse_hour_token():
    assert parse_hour_token("noon") == 12
    assert parse_hour_token("midnight") == 0
    assert parse_hour_token("1 PM") == 13
    assert parse_hour_token("14:00") == 14
    assert parse_hour_token("2am") == 2
    assert parse_hour_token("three", default_period="PM") == 15


def test_extract_hour_range_standard_cases():
    # Canonical cases from problem statement
    assert extract_hour_range_from_text("1 PM to 3 PM") == [13, 14]
    assert extract_hour_range_from_text("from noon until 2 PM") == [12, 13]
    assert extract_hour_range_from_text("between 10 AM and noon") == [10, 11]
    assert extract_hour_range_from_text("from 2 AM until 5 AM") == [2, 3, 4]
    assert extract_hour_range_from_text("6 PM until 9 PM") == [18, 19, 20]
    assert extract_hour_range_from_text("13:00 - 15:00") == [13, 14]
    assert extract_hour_range_from_text("18:00 to 22:00") == [18, 19, 20, 21]


def test_validate_and_normalize_hours():
    # Valid sorted unique
    is_valid, norm = validate_and_normalize_hours([2, 3, 4])
    assert is_valid is True
    assert norm == [2, 3, 4]

    # Deduplication and sorting
    is_valid, norm = validate_and_normalize_hours([4, 2, 3, 2])
    assert is_valid is True
    assert norm == [2, 3, 4]

    # Out of range
    is_valid, norm = validate_and_normalize_hours([22, 23, 24])
    assert is_valid is False
    assert norm == []

    # Empty list
    is_valid, norm = validate_and_normalize_hours([])
    assert is_valid is False
    assert norm == []
