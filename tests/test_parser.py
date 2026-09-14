"""
Unit tests for parser.
"""
import pytest

from src.parser import CSVParser


def test_simple_csv():
    """
    Test simple CSV parsing.
    """
    parser = CSVParser()

    csv_text = (
        "name,age\n"
        "Mie,23\n"
        "Anna,25"
    )

    expected = [
        {"name": "Mie", "age": "23"},
        {"name": "Anna", "age": "25"}
    ]

    assert parser.parse(csv_text) == expected


def test_parse_single_row() -> None:
    parser = CSVParser()

    csv_text = (
        "id,name\n"
        "1,Mie"
    )

    result = parser.parse(csv_text)

    assert result[0]["name"] == "Mie"


def test_parse_multiple_rows() -> None:
    parser = CSVParser()

    csv_text = (
        "id,name\n"
        "1,Mie\n"
        "2,Peter"
    )

    result = parser.parse(csv_text)

    assert len(result) == 2


def test_parse_empty_field() -> None:
    parser = CSVParser()

    csv_text = (
        "id,name\n"
        "1,"
    )

    result = parser.parse(csv_text)

    assert result[0]["name"] == ""


def test_empty_csv() -> None:
    parser = CSVParser()

    with pytest.raises(ValueError):
        parser.parse("")

