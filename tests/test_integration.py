"""
Integration tests using real CSV files.
"""

from src.csv_reader import CSVReader
from src.parser import CSVParser


def test_employees_file() -> None:
    """
    Verify that employees.csv can be read and parsed.
    """
    reader = CSVReader()
    parser = CSVParser()

    csv_text = reader.read("data/employees.csv")
    result = parser.parse(csv_text)

    assert len(result) > 0
    assert result[0]["name"] == "Marcus Chen"


def test_sogne_file() -> None:
    """
    Verify that sogne.csv can be read and parsed.

    Ensures that important columns from the parish dataset
    are present after parsing.
    """
    reader = CSVReader()
    parser = CSVParser()

    csv_text = reader.read("data/sogne.csv")
    result = parser.parse(csv_text)

    assert len(result) > 0

    expected_columns = {
        "dagi_id",
        "kode",
        "navn",
    }

    assert expected_columns.issubset(
        set(result[0].keys())
    )


def test_sogne_contains_data() -> None:
    """
    Verify that the parish dataset contains a large number of rows.
    """
    reader = CSVReader()
    parser = CSVParser()

    csv_text = reader.read("data/sogne.csv")
    result = parser.parse(csv_text)

    assert len(result) > 100


def test_employees_contains_expected_columns() -> None:
    """
    Verify that employees.csv contains the expected columns.
    """
    reader = CSVReader()
    parser = CSVParser()

    csv_text = reader.read("data/employees.csv")
    result = parser.parse(csv_text)

    expected_columns = {
        "name",
        "email",
        "department",
        "role",
        "salary",
        "start_date",
        "office",
    }

    assert expected_columns == set(
        result[0].keys()
    )