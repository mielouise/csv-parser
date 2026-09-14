"""
Module responsible for exporting data as JSON.
"""

import json


class JsonExporter:
    """
    Convert Python objects to JSON strings.
    """

    def to_json(
        self,
        data: list[dict[str, str]]
    ) -> str:
        """
        Convert parsed CSV data to JSON.

        Args:
            data:
                Parsed CSV data.

        Returns:
            Formatted JSON string.
        """
        return json.dumps(
            data,
            indent=4
        )