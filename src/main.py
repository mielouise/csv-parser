"""
Main program.
"""

from src.parser import CSVParser


def main():
    """
    Run parser example.
    """
    csv_text = (
        "name,age\n"
        "Mie,23\n"
        "Anna,25"
    )

    parser = CSVParser()

    result = parser.parse(csv_text)

    print(result)


if __name__ == "__main__":
    main()