"""
CSV parser module.
"""


class CSVParser:
    """
    Parse CSV-formatted text into a list of dictionaries.

    The first row is interpreted as column headers and each
    subsequent row becomes a dictionary entry.
    """

    def parse(self, text: str) -> list[dict[str, str]]:
        """
        Parse CSV data.

        Args:
            text:
                CSV-formatted text.

        Returns:
            A list of dictionaries where each dictionary
            represents a CSV row.

        Raises:
            ValueError:
                If the input is empty.
        """
        if not text.strip():
            raise ValueError("CSV input cannot be empty.")

        lines: list[str] = text.strip().splitlines()

        headers: list[str] = [
            header.strip()
            for header in lines[0].split(",")
        ]

        parsed_rows: list[dict[str, str]] = []

        for line in lines[1:]:
            values: list[str] = [
                value.strip()
                for value in line.split(",")
            ]

            row: dict[str, str] = {}

            for index, header in enumerate(headers):
                row[header] = (
                    values[index]
                    if index < len(values)
                    else ""
                )

            parsed_rows.append(row)

        return parsed_rows