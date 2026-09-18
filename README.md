# CSV Parser

A CSV parser implemented from scratch in Python.

The project was developed as part of the Specialisterne Academy Parser assignment and focuses on low-level data processing, manual CSV parsing, software architecture and automated testing.

The application reads CSV files, parses RFC 4180-inspired CSV data into Python data structures and exports the result as JSON.

---

## Project Status

- ✅ Manual CSV parser
- ✅ JSON export
- ✅ RFC 4180-inspired implementation
- ✅ Layered architecture
- ✅ 34 automated tests
- ✅ 98% code coverage
- ✅ Integration tests
- ✅ GitHub Actions CI

---

## Features

### CSV Parsing

- Manual CSV parsing
- UTF-8 file reading
- JSON export
- Missing value handling

### RFC 4180 Support

- Quoted fields
- Embedded commas
- Escaped quotes (`""`)
- Multiline fields
- Empty quoted fields
- LF line endings (`\n`)
- CRLF line endings (`\r\n`)

### Validation

The parser validates:

- Empty CSV input
- Duplicate header names
- Rows containing more values than headers
- Unclosed quoted fields

---

## Technologies

- Python 3.13
- pytest
- pytest-cov
- pathlib
- json
- Git
- GitHub Actions

---

## Project Structure

```text
src/
├── main.py
├── cli.py
├── application.py
├── csv_reader.py
├── parser.py
└── json_exporter.py

tests/
├── test_application.py
├── test_cli.py
├── test_integration.py
├── test_json.py
├── test_main.py
├── test_parser.py
└── test_reader.py

data/
├── employees.csv
└── sogne.csv
```

---

## Installation

Clone the repository:

```powershell
git clone https://github.com/mielouise/csv-parser
cd csv-parser
```

Create and activate a virtual environment:

```powershell
python -m venv .venv

.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## Running the Application

Run from the project root:

```powershell
python -m src.main
```

The application presents a file-selection menu:

```text
1. employees.csv
2. sogne.csv
3. Custom CSV file
```

After selecting a file, the parsed CSV data is displayed as JSON.

---

## Example

### Input

```csv
id,name
1,Mie
2,Anna
```

### Output

```json
[
    {
        "id": "1",
        "name": "Mie"
    },
    {
        "id": "2",
        "name": "Anna"
    }
]
```

---

## Software Architecture

The application follows a layered architecture.

```text
main.py
    ↓
cli.py
    ↓
application.py
    ↓
csv_reader.py
parser.py
json_exporter.py
```

### Responsibilities

| Component | Responsibility |
|------------|----------------|
| `main.py` | Application entry point |
| `CLI` | User interaction and error presentation |
| `CSVApplication` | Workflow coordination |
| `CSVReader` | File access |
| `CSVParser` | Parsing and validation |
| `JsonExporter` | JSON serialization |

### Design Principles

- Separation of Concerns
- Composition
- Single Responsibility Principle
- Test-Driven Development mindset

---

## Design Decisions

### Manual CSV Parsing

The parser was intentionally implemented without Python's built-in `csv` module.

The goal was to gain practical experience with:

- Raw data processing
- Parsing algorithms
- RFC interpretation
- Handling malformed data
- Automated testing

### Composition

`CSVApplication` acts as the application's service layer and coordinates:

```text
CSVApplication
├── CSVReader
├── CSVParser
└── JsonExporter
```

This approach improves maintainability, readability and testability.

---

## RFC 4180 Support

The parser supports the most relevant RFC 4180 behaviors.

### Embedded Commas

```csv
name,address
Mie,"Odense, Denmark"
```

### Escaped Quotes

```csv
text
"He said ""Hello"""
```

Output:

```text
He said "Hello"
```

### Multiline Fields

```csv
description
"Line 1
Line 2"
```

### Empty Quoted Fields

```csv
name
""
```

Output:

```json
[
    {
        "name": ""
    }
]
```

---

## Validation Rules

The parser rejects malformed CSV input.

### Duplicate Headers

```csv
name,name
Mie,Anna
```

### More Values Than Headers

```csv
id,name
1,Mie,Odense
```

### Unclosed Quoted Fields

```csv
name,comment
Mie,"Hello
```

### Empty Input

```csv

```

---

## Error Handling

Errors are detected by the component responsible for the operation and propagated upward.

### CSVReader

May raise:

- `FileNotFoundError`
- `PermissionError`
- `UnicodeDecodeError`

### CSVParser

May raise:

- `ValueError`

### CLI

Responsible for converting exceptions into user-friendly error messages.

This keeps parsing logic independent from presentation logic.

---

## Testing

Run all tests:

```powershell
python -m pytest
```

Generate a coverage report:

```powershell
python -m pytest --cov=src --cov-report=term-missing
```

### Results

- 34 passing tests
- 98% code coverage

The project exceeds the assignment requirement of **95% code coverage**.

### Test Coverage

The test suite includes:

- Unit tests
- Integration tests
- RFC 4180 test cases
- Validation tests
- Edge case tests

---

## Continuous Integration

GitHub Actions automatically:

- Runs all tests
- Verifies the coverage requirement
- Detects regressions

The workflow executes on every push and pull request.

---

## UML Diagram

The following UML class diagram illustrates the
architecture of the application and the relationships
between its core components.

docs/uml-diagram.png

The diagram illustrates the relationships between:

- CLI
- CSVApplication
- CSVReader
- CSVParser
- JsonExporter

and documents the layered architecture used by the application.
---


## Future Improvements

Potential future enhancements include:

- Additional RFC 4180 compatibility
- Configurable delimiters
- Direct JSON file output
- Logging support
- Command-line arguments

---

## Author

**Mie Louise Nielsen**

Developed as part of the Specialisterne Academy Parser assignment with a focus on software architecture, raw data processing and automated testing.