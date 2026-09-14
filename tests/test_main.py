"""
Unit tests for the main module.
"""

from pathlib import Path

import pytest

from src import main
from src.main import get_file_path


def test_get_employees_path(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Verify employees.csv selection.
    """
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1"
    )

    assert (
        get_file_path()
        == Path("data/employees.csv")
    )


def test_get_sogne_path(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Verify sogne.csv selection.
    """
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2"
    )

    assert (
        get_file_path()
        == Path("data/sogne.csv")
    )


def test_get_custom_path(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Verify custom file path selection.
    """
    responses = iter(
        [
            "3",
            "custom/test.csv",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(responses)
    )

    assert (
        get_file_path()
        == Path("custom/test.csv")
    )


def test_invalid_choice(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Verify invalid menu option raises ValueError.
    """
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "99"
    )

    with pytest.raises(ValueError):
        get_file_path()


def test_main(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Verify that main() reads, parses and prints data.
    """

    def mock_read(
        _self,
        _file_path: str
    ) -> str:
        return (
            "id,name\n"
            "1,Mie"
        )

    monkeypatch.setattr(
        "src.main.CSVReader.read",
        mock_read
    )

    monkeypatch.setattr(
        "src.main.get_file_path",
        lambda: Path("dummy.csv")
    )

    main.main()

    captured = capsys.readouterr()

    assert "Mie" in captured.out


def test_main_file_not_found(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Verify FileNotFoundError handling.
    """

    def mock_read(
        _self,
        _file_path: str
    ) -> str:
        raise FileNotFoundError()

    monkeypatch.setattr(
        "src.main.CSVReader.read",
        mock_read
    )

    monkeypatch.setattr(
        "src.main.get_file_path",
        lambda: Path("missing.csv")
    )

    main.main()

    captured = capsys.readouterr()

    assert "not found" in captured.out.lower()


def test_main_value_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Verify parser ValueError handling.
    """

    def mock_read(
        _self,
        _file_path: str
    ) -> str:
        return ""

    monkeypatch.setattr(
        "src.main.CSVReader.read",
        mock_read
    )

    monkeypatch.setattr(
        "src.main.get_file_path",
        lambda: Path("test.csv")
    )

    main.main()

    captured = capsys.readouterr()

    assert "csv parsing error" in (
        captured.out.lower()
    )