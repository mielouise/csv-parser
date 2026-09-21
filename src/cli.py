"""
Command-line interface module.

Handles:

- User interaction
- File selection
- User-facing error handling
"""

from pathlib import Path

from src.application import CSVApplication


DATA_DIRECTORY: Path = Path("data")


class CLI:
    """
    Provide the command-line interface.

    Responsible for:

    - User interaction
    - File selection
    - Presenting errors to the user
    """

    EMPLOYEES_FILE: Path = (
        DATA_DIRECTORY / "employees.csv"
    )

    SOGNE_FILE: Path = (
        DATA_DIRECTORY / "sogne.csv"
    )

    def __init__(self) -> None:
        """
        Initialize application services.
        """
        self._application = CSVApplication()

    def run(self) -> None:
        """
        Run the application.

        Coordinates file selection and CSV
        processing while handling user-facing
        errors.
        """
        try:
            file_path: Path = (
                self._get_file_path()
            )

            json_output: str = (
                self._application.process_file(
                    file_path
                )
            )

            print(json_output)
            output_path = file_path.with_suffix(".json")
            self._application.export_file(
                file_path,
                output_path,
            )
            print(
                f"\nJSON file written to: "
                f"{output_path}"
            )

        except FileNotFoundError:
            print(
                f"Error: File '{file_path}' "
                "was not found."
            )

        except PermissionError:
            print(
                f"Error: Access denied to "
                f"'{file_path}'."
            )

        except UnicodeDecodeError:
            print(
                "Error: Unsupported file "
                "encoding."
            )

        except ValueError as error:
            print(
                f"CSV validation error: "
                f"{error}"
            )

        except Exception as error:
            print(
                f"Unexpected error: {error}"
            )

    def _get_file_path(self) -> Path:
        """
        Let the user choose a CSV file.

        Returns:
            Path to the selected CSV file.

        Raises:
            ValueError:
                If an invalid menu option is
                entered.
        """
        self._print_menu()

        choice: str = input(
            "\nEnter your choice (1-3): "
        ).strip()

        if choice == "1":
            return self.EMPLOYEES_FILE

        if choice == "2":
            return self.SOGNE_FILE

        if choice == "3":
            return self._get_custom_file_path()

        raise ValueError(
            "Invalid menu choice."
        )

    def _get_custom_file_path(self) -> Path:
        """
        Read a custom file path from the user.

        Returns:
            Path entered by the user.
        """
        return Path(
            input(
                "Enter the path to your CSV file: "
            ).strip()
        )

    def _print_menu(self) -> None:
        """
        Display the file selection menu.
        """
        print("\nChoose a CSV file:")
        print("1. employees.csv")
        print("2. sogne.csv")
        print("3. Custom CSV file")


def run() -> None:
    """
    Start the command-line interface.
    """
    CLI().run()