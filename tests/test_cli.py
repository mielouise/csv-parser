"""
Unit tests for the command-line interface.
"""

from pathlib import Path

import pytest

from src.cli import CLI


def test_get_employees_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Verify selection of employees.csv.
    """
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1"
    )

    cli = CLI()

    assert (
        cli._get_file_path()
        == cli.EMPLOYEES_FILE
    )


def test_get_sogne_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Verify selection of sogne.csv.
    """
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2"
    )

    cli = CLI()

    assert (
        cli._get_file_path()
        == cli.SOGNE_FILE
    )


def test_get_custom_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Verify selection of a custom file.
    """
    responses = iter(
        [
            "3",
            "custom.csv",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(responses)
    )

    cli = CLI()

    assert (
        cli._get_file_path()
        == Path("custom.csv")
    )


def test_invalid_menu_choice(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Verify invalid menu choice handling.
    """
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "99"
    )

    cli = CLI()

    with pytest.raises(ValueError):
        cli._get_file_path()


def test_run_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Verify successful execution.
    """
    cli = CLI()

    monkeypatch.setattr(
        cli,
        "_get_file_path",
        lambda: Path("dummy.csv")
    )

    monkeypatch.setattr(
        cli._application,
        "process_file",
        lambda _path: '{"name": "Mie"}'
    )

    cli.run()

    captured = capsys.readouterr()

    assert "Mie" in captured.out


def test_run_file_not_found(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Verify handling of missing files.
    """
    cli = CLI()

    monkeypatch.setattr(
        cli,
        "_get_file_path",
        lambda: Path("missing.csv")
    )

    def mock_process(
        _path: Path,
    ) -> str:
        raise FileNotFoundError

    monkeypatch.setattr(
        cli._application,
        "process_file",
        mock_process
    )

    cli.run()

    captured = capsys.readouterr()

    assert "not found" in captured.out.lower()


def test_run_validation_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Verify CSV validation error handling.
    """
    cli = CLI()

    monkeypatch.setattr(
        cli,
        "_get_file_path",
        lambda: Path("invalid.csv")
    )

    def mock_process(
        _path: Path,
    ) -> str:
        raise ValueError(
            "Duplicate header names."
        )

    monkeypatch.setattr(
        cli._application,
        "process_file",
        mock_process
    )

    cli.run()

    captured = capsys.readouterr()

    assert (
        "validation"
        in captured.out.lower()
    )


def test_run_permission_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Verify permission error handling.
    """
    cli = CLI()

    monkeypatch.setattr(
        cli,
        "_get_file_path",
        lambda: Path("restricted.csv")
    )

    def mock_process(
        _path: Path,
    ) -> str:
        raise PermissionError

    monkeypatch.setattr(
        cli._application,
        "process_file",
        mock_process
    )

    cli.run()

    captured = capsys.readouterr()

    assert (
        "access denied"
        in captured.out.lower()
    )


def test_run_unexpected_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Verify handling of unexpected errors.
    """
    cli = CLI()

    monkeypatch.setattr(
        cli,
        "_get_file_path",
        lambda: Path("unexpected.csv")
    )

    def mock_process(
        _path: Path,
    ) -> str:
        raise RuntimeError(
            "Unexpected failure."
        )

    monkeypatch.setattr(
        cli._application,
        "process_file",
        mock_process
    )

    cli.run()

    captured = capsys.readouterr()

    assert (
        "unexpected"
        in captured.out.lower()
    )