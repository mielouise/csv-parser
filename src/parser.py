"""
CSV parser module.

Implements a simple CSV parser inspired by RFC 4180.

Supported features:
- Header row
- Quoted fields
- Commas within quoted fields
- Escaped double quotes ("")
- Empty fields
- LF and CRLF line endings
"""


class CSVParser:
    """
    Parse CSV-formatted text into a list of dictionaries.

    The first row is treated as column headers.
    """

    def parse(self, text: str) -> list[dict[str, str]]:
        """
        Parse CSV text into Python objects.

        Args:
            text:
                CSV-formatted text.

        Returns:
            A list of dictionaries where each dictionary
            represents a row in the CSV data.

        Raises:
            ValueError:
                If input is empty or malformed.
        """
        if not text.strip():
            raise ValueError("CSV input cannot be empty.")

        rows: list[list[str]] = self._parse_rows(text)

        if not rows:
            raise ValueError("No CSV rows found.")

        headers: list[str] = [
            header.strip()
            for header in rows[0]
        ]

        parsed_rows: list[dict[str, str]] = []

        for values in rows[1:]:
            row: dict[str, str] = {}

            for index, header in enumerate(headers):
                row[header] = (
                    values[index]
                    if index < len(values)
                    else ""
                )

            parsed_rows.append(row)

        return parsed_rows

    def _parse_rows(self, text: str) -> list[list[str]]:
        """
        Parse CSV text into rows and fields.

        Args:
            text:
                CSV-formatted text.

        Returns:
            A list of rows where each row is a list of fields.
        """
        rows: list[list[str]] = []

        current_row: list[str] = []
        current_field: list[str] = []

        inside_quotes: bool = False

        index: int = 0

        while index < len(text):
            character: str = text[index]

            if character == '"':
                if inside_quotes:
                    next_character_exists = (
                        index + 1 < len(text)
                    )

                    if (
                        next_character_exists
                        and text[index + 1] == '"'
                    ):
                        current_field.append('"')
                        index += 1
                    else:
                        inside_quotes = False
                else:
                    inside_quotes = True

            elif character == "," and not inside_quotes:
                current_row.append(
                    "".join(current_field)
                )
                current_field = []

            elif character in ("\n", "\r") and not inside_quotes:
                if (
                    character == "\r"
                    and index + 1 < len(text)
                    and text[index + 1] == "\n"
                ):
                    index += 1

                current_row.append(
                    "".join(current_field)
                )

                rows.append(current_row)

                current_row = []
                current_field = []

            else:
                current_field.append(character)

            index += 1

        if inside_quotes:
            raise ValueError(
                "Malformed CSV: unclosed quoted field."
            )

        current_row.append(
            "".join(current_field)
        )

        if current_row:
            rows.append(current_row)

        return rows