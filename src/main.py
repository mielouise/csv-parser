"""
Application entry point.
"""

from src.application import CSVApplication


def main() -> None:
    """
    Run the CSV application.
    """
    CSVApplication().run()


if __name__ == "__main__":
    main()