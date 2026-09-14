"""
Application entry point.
"""

from pathlib import Path
import sys

from src.csv_reader import CSVReader
from src.json_exporter import JsonExporter
from src.parser import CSVParser


def get_file_path() -> Path:
    """
    Let the user choose a CSV file.

    Returns:
        Path to the selected CSV file.

    Raises:
        ValueError:
            If an invalid menu choice is entered.
    """
    print("\nChoose a CSV file:")
    print("1. employees.csv")
    print("2. sogne.csv")
    print("3. Custom CSV file")

    choice = input(
        "\nEnter your choice (1-3): "
    ).strip()

    if choice == "1":
        return Path("data/employees.csv")

    if choice == "2":
        return Path("data/sogne.csv")

    if choice == "3":
        return Path(
            input(
                "Enter the path to your CSV file: "
            ).strip()
        )

    raise ValueError("Invalid choice.")


def main() -> None:
    """
    Run the CSV parser application.
    """
    reader = CSVReader()
    parser = CSVParser()
    exporter = JsonExporter()

    try:
        if len(sys.argv) > 1:
            file_path = Path(sys.argv[1])
        else:
            file_path = get_file_path()

        csv_text = reader.read(str(file_path))

        parsed_data = parser.parse(csv_text)

        json_output = exporter.to_json(parsed_data)

        print(json_output)

    except FileNotFoundError:
        print(
            f"Error: File '{file_path}' was not found."
        )

    except ValueError as error:
        print(
            f"CSV parsing error: {error}"
        )

    except Exception as error:
        print(
            f"Unexpected error: {error}"
        )


if __name__ == "__main__":
    main()