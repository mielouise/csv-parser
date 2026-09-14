from src.main import get_file_path


def test_get_employees_path(
    monkeypatch
) -> None:
    """
    Test employees.csv selection.
    """
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1"
    )

    assert (
        get_file_path()
        == "data/employees.csv"
    )


def test_get_sogne_path(
    monkeypatch
) -> None:
    """
    Test sogne.dawa.csv selection.
    """
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2"
    )

    assert (
        get_file_path()
        == "data/sogne.dawa.csv"
    )