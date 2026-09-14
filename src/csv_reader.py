"""
Module responsible for reading CSV files.
"""


class CSVReader:
    """
    Read CSV data from a file.
    """

    def read(self, file_path: str) -> str:
        """
        Read a file and return its contents.

        Args:
            file_path:
                Path to the CSV file.

        Returns:
            The file contents as a string.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()