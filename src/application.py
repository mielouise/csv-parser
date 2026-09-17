"""
Application service layer.

Coordinates the CSV processing workflow.
"""

from pathlib import Path

from src.csv_reader import CSVReader
from src.json_exporter import JsonExporter
from src.parser import CSVParser


class CSVApplication:
    """
    Coordinate the CSV processing workflow.

    Acts as a facade over the application's
    core components.
    """

    def __init__(self) -> None:
        """
        Initialize application dependencies.
        """
        self._reader = CSVReader()
        self._parser = CSVParser()
        self._exporter = JsonExporter()

    def process_file(self,file_path: Path,) -> str:
        """
        Process a CSV file and return JSON output.

        The workflow consists of:

        1. Reading CSV data.
        2. Parsing CSV content.
        3. Exporting parsed data as JSON.

        Args:
            file_path:
                Path to a CSV file.

        Returns:
            JSON representation of the CSV data.

        Raises:
            FileNotFoundError:
                If the file cannot be found.

            ValueError:
                If CSV validation fails.
        """
        csv_text = self._reader.read(file_path)

        parsed_data = self._parser.parse(csv_text)

        return self._exporter.to_json(parsed_data)