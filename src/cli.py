"""
Command-line interface module.

Handles user interaction, file selection and
user-facing error handling.
"""

from pathlib import Path

from src.application import CSVApplication


DATA_DIRECTORY: Path = Path("data")


class CLI:
    """
    Provide a command-line interface for the
    CSV parser application.
    """

    EMPLOYEES_FILE: Path = (
        DATA_DIRECTORY / "employees.csv"
    )

    SOGNE_FILE: Path = (
        DATA_DIRECTORY / "sogne.csv"
    )

    def __init__(self) -> None:
        """
        Initialize the command-line interface.
        """
        self.application = CSVApplication()

    def run(self) -> None:
        """
        Run the application.

        Coordinates file selection and CSV
        processing while handling user-facing
        errors.
        """
        try:
            file_path = self._get_file_path()

            json_output = (
                self.application.process_file(
                    file_path
                )
            )

            print(json_output)

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

    def _get_file_path(self) -> Path:
        """
        Let the user select a CSV file.

        Returns:
            Path to the selected CSV file.

        Raises:
            ValueError:
                If an invalid menu choice
                is entered.
        """
        self._print_menu()

        choice = input(
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
