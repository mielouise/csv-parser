"""
Unit tests for CSVParser.
"""

import pytest

from src.parser import CSVParser


def test_simple_csv() -> None:
    """
    Test parsing of a simple CSV file.
    """
    parser = CSVParser()

    csv_text = (
        "name,age\n"
        "Mie,23\n"
        "Anna,25"
    )

    expected = [
        {"name": "Mie", "age": "23"},
        {"name": "Anna", "age": "25"},
    ]

    assert parser.parse(csv_text) == expected


def test_parse_single_row() -> None:
    """
    Test parsing of a single data row.
    """
    parser = CSVParser()

    csv_text = (
        "id,name\n"
        "1,Mie"
    )

    result = parser.parse(csv_text)

    assert result[0]["name"] == "Mie"


def test_parse_multiple_rows() -> None:
    """
    Test parsing of multiple rows.
    """
    parser = CSVParser()

    csv_text = (
        "id,name\n"
        "1,Mie\n"
        "2,Peter"
    )

    result = parser.parse(csv_text)

    assert len(result) == 2


def test_parse_empty_field() -> None:
    """
    Test parsing of empty fields.
    """
    parser = CSVParser()

    csv_text = (
        "name,age\n"
        "Mie,"
    )

    expected = [
        {
            "name": "Mie",
            "age": "",
        }
    ]

    assert parser.parse(csv_text) == expected


def test_missing_columns() -> None:
    """
    Test rows with missing columns.
    """
    parser = CSVParser()

    csv_text = (
        "id,name,email\n"
        "1,Mie"
    )

    expected = [
        {
            "id": "1",
            "name": "Mie",
            "email": "",
        }
    ]

    assert parser.parse(csv_text) == expected


def test_empty_csv() -> None:
    """
    Test that empty input raises ValueError.
    """
    parser = CSVParser()

    with pytest.raises(ValueError):
        parser.parse("")


def test_comma_inside_quotes() -> None:
    """
    Test commas inside quoted fields.
    """
    parser = CSVParser()

    csv_text = (
        'name,address\n'
        'Mie,"Odense, Denmark"'
    )

    expected = [
        {
            "name": "Mie",
            "address": "Odense, Denmark",
        }
    ]

    assert parser.parse(csv_text) == expected


def test_escaped_quotes() -> None:
    """
    Test escaped double quotes.
    """
    parser = CSVParser()

    csv_text = (
        'text\n'
        '"He said ""Hello"""'
    )

    expected = [
        {
            "text": 'He said "Hello"',
        }
    ]

    assert parser.parse(csv_text) == expected


def test_multiline_field() -> None:
    """
    Test multiline quoted fields.
    """
    parser = CSVParser()

    csv_text = (
        'description\n'
        '"Line 1\n'
        'Line 2"'
    )

    expected = [
        {
            "description": "Line 1\nLine 2",
        }
    ]

    assert parser.parse(csv_text) == expected


def test_duplicate_headers() -> None:
    """
    Test duplicate headers raise ValueError.
    """
    parser = CSVParser()

    csv_text = (
        "name,name\n"
        "Mie,Peter"
    )

    with pytest.raises(ValueError):
        parser.parse(csv_text)


def test_extra_columns() -> None:
    """
    Test rows with too many columns.
    """
    parser = CSVParser()

    csv_text = (
        "id,name\n"
        "1,Mie,Odense"
    )

    with pytest.raises(ValueError):
        parser.parse(csv_text)


def test_unclosed_quotes() -> None:
    """
    Test malformed quoted fields.
    """
    parser = CSVParser()

    csv_text = (
        'name,comment\n'
        'Mie,"Hello'
    )

    with pytest.raises(ValueError):
        parser.parse(csv_text)

def test_crlf_line_endings() -> None:
    """
    Test Windows CRLF line endings.
    """
    parser = CSVParser()

    csv_text = (
        "name,age\r\n"
        "Mie,23\r\n"
        "Anna,25"
    )

    result = parser.parse(csv_text)

    assert len(result) == 2