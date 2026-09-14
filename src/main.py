"""
Application entry point.
"""

from src.csv_reader import CSVReader
from src.json_exporter import JsonExporter
from src.parser import CSVParser


def main() -> None:
    """
    Run the CSV parser application.
    """
    reader = CSVReader()
    parser = CSVParser()
    exporter = JsonExporter()

    csv_text = reader.read("data/employees.csv")

    parsed_data = parser.parse(csv_text)

    json_output = exporter.to_json(parsed_data)

    print(json_output)


if __name__ == "__main__":
    main()
