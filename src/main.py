"""
Application entry point.
"""

from src.csv_reader import CSVReader
from src.json_exporter import JsonExporter
from src.parser import CSVParser


def get_file_path() -> str:
    """
    Let the user choose a CSV file.

    Returns:
        Path to the selected CSV file.

    Raises:
        ValueError:
            If an invalid option is entered.
    """
    print("\nChoose a CSV file:")
    print("1. employees.csv")
    print("2. sogne.csv")
    print("3. Custom CSV file")

    choice = input(
        "\nEnter your choice (1-3): "
    ).strip()

    if choice == "1":
        return "data/employees.csv"

    if choice == "2":
        return "data/sogne.csv"

    if choice == "3":
        return input(
            "Enter the path to your CSV file: "
        ).strip()

    raise ValueError("Invalid choice.")


def main() -> None:
    """
    Run the CSV parser application.
    """
    reader = CSVReader()
    parser = CSVParser()
    exporter = JsonExporter()

    try:
        file_path = get_file_path()

        csv_text = reader.read(file_path)

        parsed_data = parser.parse(csv_text)

        json_output = exporter.to_json(parsed_data)

        print(json_output)

    except FileNotFoundError:
        print("Error: File not found.")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()