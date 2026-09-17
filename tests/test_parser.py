"""
Unit tests for CSVParser.

These tests verify:

- Basic CSV parsing
- RFC 4180-compliant field handling
- CSV validation rules
- Edge cases and malformed input
- Robust handling of imperfect data
"""

import pytest

from src.parser import CSVParser


def test_simple_csv() -> None:
    """
    Verify parsing of a simple CSV document.

    A valid CSV file containing multiple rows should
    produce a list of dictionaries.
    """
    parser = CSVParser()

    csv_text = (
        "name,age\n"
        "Mie,23\n"
        "Anna,25"
    )

    expected = [
        {
            "name": "Mie",
            "age": "23",
        },
        {
            "name": "Anna",
            "age": "25",
        },
    ]

    assert parser.parse(csv_text) == expected


def test_parse_single_row() -> None:
    """
    Verify parsing of a single data row.
    """
    parser = CSVParser()

    csv_text = (
        "id,name\n"
        "1,Mie"
    )

    result = parser.parse(csv_text)

    assert result == [
        {
            "id": "1",
            "name": "Mie",
        }
    ]


def test_parse_multiple_rows() -> None:
    """
    Verify parsing of multiple data rows.
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
    Verify that empty fields are preserved.

    Empty CSV values should be represented as
    empty strings.
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
    Verify handling of rows with fewer values
    than headers.

    Missing values should be populated with
    empty strings.
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
    Verify that empty input is rejected.

    Empty CSV content should raise ValueError.
    """
    parser = CSVParser()

    with pytest.raises(ValueError):
        parser.parse("")


def test_comma_inside_quotes() -> None:
    """
    Verify that commas inside quoted fields are
    treated as field content rather than delimiters.

    This behavior is required by RFC 4180.
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
    Verify handling of escaped quotation marks.

    RFC 4180 represents embedded quotation marks
    using two consecutive quote characters ("").
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
    Verify preservation of line breaks inside
    quoted fields.

    RFC 4180 allows quoted fields to span
    multiple lines.
    """
    parser = CSVParser()

    csv_text = (
        'description\n'
        '"Line 1\n'
        'Line 2"'
    )

    expected = [
        {
            "description": (
                "Line 1\n"
                "Line 2"
            ),
        }
    ]

    assert parser.parse(csv_text) == expected


def test_duplicate_headers() -> None:
    """
    Verify that duplicate headers are rejected.

    The parser uses a dictionary-based data
    structure and therefore requires unique
    column names.
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
    Verify rejection of rows containing
    more values than headers.
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
    Verify detection of malformed quoted fields.

    Unclosed quoted fields should raise
    ValueError.
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
    Verify support for Windows CRLF line endings.
    """
    parser = CSVParser()

    csv_text = (
        "name,age\r\n"
        "Mie,23\r\n"
        "Anna,25"
    )

    result = parser.parse(csv_text)

    assert result == [
        {
            "name": "Mie",
            "age": "23",
        },
        {
            "name": "Anna",
            "age": "25",
        },
    ]


def test_ignore_trailing_empty_row() -> None:
    """
    Verify that trailing blank lines do not
    create additional records.
    """
    parser = CSVParser()

    csv_text = (
        "name,age\n"
        "Mie,23\n"
    )

    result = parser.parse(csv_text)

    assert len(result) == 1


def test_header_only() -> None:
    """
    Verify handling of a CSV document
    containing only headers.

    A file without data rows should produce
    an empty result set.
    """
    parser = CSVParser()

    result = parser.parse(
        "id,name"
    )

    assert result == []


def test_empty_quoted_field() -> None:
    """
    Verify parsing of empty quoted fields.

    Empty quoted fields should be converted
    to empty strings.
    """
    parser = CSVParser()

    csv_text = (
        'name\n'
        '""'
    )

    expected = [
        {
            "name": "",
        }
    ]

    assert parser.parse(csv_text) == expected


def test_mixed_line_endings() -> None:
    """
    Verify handling of mixed LF and CRLF
    line endings.

    Real-world CSV files sometimes contain
    inconsistent line endings.
    """
    parser = CSVParser()

    csv_text = (
        "id,name\r\n"
        "1,Mie\n"
        "2,Anna\r\n"
    )

    result = parser.parse(csv_text)

    assert result == [
        {
            "id": "1",
            "name": "Mie",
        },
        {
            "id": "2",
            "name": "Anna",
        },
    ]