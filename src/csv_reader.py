"""
Module responsible for reading CSV files.
"""

from pathlib import Path


class CSVReader:
    """
    Read CSV data from files.
    """

    def read(self, file_path: str | Path) -> str:
        """
        Read a CSV file and return its contents.

        Args:
            file_path:
                Path to the CSV file.

        Returns:
            The file contents as a string.
        """
        path = Path(file_path)

        with path.open(
            "r",
            encoding="utf-8"
        ) as file:
            return file.read()