import json

from src.json_exporter import JsonExporter


def test_json_export() -> None:
    """
    Verify JSON conversion.
    """
    exporter = JsonExporter()

    data = [
        {
            "name": "Mie"
        }
    ]

    json_string = exporter.to_json(data)

    parsed = json.loads(json_string)

    assert parsed == {
        "rows": [
            {
                "name": "Mie"
            }
        ]
    }


def test_json_export_to_file(tmp_path) -> None:
    """
    Verify structured JSON can be written to a file.
    """
    exporter = JsonExporter()
    output_path = tmp_path / "employees.json"

    exporter.to_file(
        [{"name": "Mie"}],
        output_path,
        root_key="employees",
    )

    parsed = json.loads(
        output_path.read_text(encoding="utf-8")
    )

    assert parsed == {
        "employees": [
            {
                "name": "Mie"
            }
        ]
    }