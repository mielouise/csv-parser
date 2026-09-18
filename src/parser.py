"""
CSV parser module.

Implements a CSV parser inspired by RFC 4180.
"""


class CSVParser:
    """
    Parse CSV-formatted text into a list of dictionaries.

    The first row is interpreted as column headers.
    Data rows are returned as dictionaries where
    header names map to field values.
    """

    def parse(
        self,
        text: str,
    ) -> list[dict[str, str]]:
        """
        Parse CSV-formatted text.

        Args:
            text:
                CSV-formatted text.

        Returns:
            A list of dictionaries representing CSV rows.

        Raises:
            ValueError:
                If the input is empty.

            ValueError:
                If duplicate headers are detected.

            ValueError:
                If a row contains more values than headers.
        """
        if not text.strip():
            raise ValueError(
                "CSV input cannot be empty."
            )

        rows: list[list[str]] = (
            self._parse_rows(text)
        )

        headers: list[str] = rows[0]

        if len(headers) != len(set(headers)):
            raise ValueError(
                "Duplicate header names are not allowed."
            )

        parsed_rows: list[
            dict[str, str]
        ] = []

        for row_values in rows[1:]:
            if len(row_values) > len(headers):
                raise ValueError(
                    "More values than headers in CSV row."
                )

            row: dict[str, str] = {}

            for index, header in enumerate(headers):
                row[header] = (
                    row_values[index]
                    if index < len(row_values)
                    else ""
                )

            parsed_rows.append(row)

        return parsed_rows

    def _parse_rows(
        self,
        text: str,
    ) -> list[list[str]]:
        """
        Parse CSV text into rows and fields.

        Supported features:

        - Quoted fields
        - Embedded commas
        - Escaped quotes ("")
        - Multiline fields
        - Empty quoted fields ("")
        - LF line endings
        - CRLF line endings

        Args:
            text:
                CSV-formatted text.

        Returns:
            Parsed rows and fields.

        Raises:
            ValueError:
                If a quoted field is not properly closed.
        """
        rows: list[list[str]] = []

        current_row: list[str] = []
        current_field: list[str] = []

        inside_quotes: bool = False
        row_has_content: bool = False

        index: int = 0

        while index < len(text):
            character: str = text[index]

            if character == '"':
                row_has_content = True

                if inside_quotes:
                    if (
                        index + 1 < len(text)
                        and text[index + 1] == '"'
                    ):
                        current_field.append('"')
                        index += 1
                    else:
                        inside_quotes = False
                else:
                    inside_quotes = True

            elif (
                character == ","
                and not inside_quotes
            ):
                current_row.append(
                    "".join(current_field)
                )

                current_field = []

            elif (
                character in ("\n", "\r")
                and not inside_quotes
            ):
                if (
                    character == "\r"
                    and index + 1 < len(text)
                    and text[index + 1] == "\n"
                ):
                    index += 1

                current_row.append(
                    "".join(current_field)
                )

                if (
                    row_has_content
                    or any(
                        field.strip()
                        for field in current_row
                    )
                ):
                    rows.append(current_row)

                current_row = []
                current_field = []
                row_has_content = False

            else:
                current_field.append(character)

                if character.strip():
                    row_has_content = True

            index += 1

        if inside_quotes:
            raise ValueError(
                "Malformed CSV: unclosed quoted field."
            )

        current_row.append(
            "".join(current_field)
        )

        if (
            row_has_content
            or any(
                field.strip()
                for field in current_row
            )
        ):
            rows.append(current_row)

        return rows