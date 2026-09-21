"""
Module responsible for exporting data as JSON.
"""

import json
from pathlib import Path


class JsonExporter:
    """
    Convert Python objects to structured JSON strings and files.
    """

    def to_json(
        self,
        data: list[dict[str, str]],
        root_key: str = "rows",
    ) -> str:
        """
        Convert parsed CSV data to structured JSON.

        Args:
            data:
                Parsed CSV data.

            root_key:
                Name of the top-level JSON property.

        Returns:
            Formatted JSON string.
        """
        return json.dumps(
            {root_key: data},
            indent=4,
            ensure_ascii=False,
        )

    def to_file(
        self,
        data: list[dict[str, str]],
        file_path: str | Path,
        root_key: str = "rows",
    ) -> None:
        """
        Write parsed CSV data as structured JSON to a file.
        """
        path = Path(file_path)

        with path.open("w", encoding="utf-8") as file:
            json.dump(
                {root_key: data},
                file,
                indent=4,
                ensure_ascii=False,
            )