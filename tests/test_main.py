from src import main


def test_main(monkeypatch, capsys) -> None:
    """
    Verify that main() processes CSV data correctly.
    """

    def mock_read(self, file_path: str) -> str:
        return (
            "id,name\n"
            "1,Mie"
        )

    monkeypatch.setattr(
        "src.main.CSVReader.read",
        mock_read
    )

    main.main()

    captured = capsys.readouterr()

    assert "Mie" in captured.out