"""
Unit tests for the application service layer.
"""

from pathlib import Path

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

    assert "Mie" in result
    assert '"name"' in result


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