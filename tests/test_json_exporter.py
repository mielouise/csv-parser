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

    assert '"name": "Mie"' in json_string