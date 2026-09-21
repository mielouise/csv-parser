"""
Unit tests for the application service layer.
"""

from pathlib import Path

import json

from src.application import CSVApplication


def test_process_file(
    monkeypatch
) -> None:
    """
    Verify that a CSV file can be processed
    and exported as JSON.
    """

    def mock_read(
        self,
        file_path: Path
    ) -> str:
        return (
            "id,name\n"
            "1,Mie"
        )

    monkeypatch.setattr(
        "src.application.CSVReader.read",
        mock_read
    )

    application = CSVApplication()

    result = application.process_file(
        Path("dummy.csv")
    )

    assert json.loads(result) == {
        "dummy": [
            {
                "id": "1",
                "name": "Mie",
            }
        ]
    }


def test_export_file(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """
    Verify that parsed CSV data is exported to JSON.
    """
    monkeypatch.setattr(
        "src.application.CSVReader.read",
        lambda self, file_path: "id,name\n1,Mie",
    )

    application = CSVApplication()
    output_path = tmp_path / "employees.json"

    application.export_file(
        Path("employees.csv"),
        output_path,
    )

    assert json.loads(
        output_path.read_text(encoding="utf-8")
    ) == {
        "employees": [
            {
                "id": "1",
                "name": "Mie",
            }
        ]
    }


def test_process_file_file_not_found(
    monkeypatch
) -> None:
    """
    Verify FileNotFoundError propagation.
    """

    def mock_read(
        self,
        file_path: Path
    ) -> str:
        raise FileNotFoundError

    monkeypatch.setattr(
        "src.application.CSVReader.read",
        mock_read
    )

    application = CSVApplication()

    try:
        application.process_file(
            Path("missing.csv")
        )
        assert False
    except FileNotFoundError:
        assert True