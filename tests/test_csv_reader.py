from pathlib import Path

from src.csv_reader import CSVReader


def test_read_file(tmp_path: Path) -> None:
    """
    Verify that a file can be read correctly.
    """
    csv_file = tmp_path / "test.csv"

    csv_file.write_text(
        "id,name\n1,Mie",
        encoding="utf-8"
    )

    reader = CSVReader()

    content = reader.read(csv_file)

    assert "Mie" in content