# CDI Manager

A book loan management platform for a primary school. Built as part of a NSI (Computer Science) assignment — French high school, Year 11.

The app handles students, books, and loans — a student can only borrow one book at a time.

## NSI Assignment Scope

The assessed part of this project covers:

- `data/` — data models and CSV access layer
- `cli/` — command-line interface
- `tests/data/` and `tests/cli/` — related tests

Everything else (Flask API, HTML/CSS/JS frontend) is a bonus and reflects the author's personal interest. The examiner is welcome to explore it.

## Stack

- **Backend**: Python 3.14, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data**: CSV files
- **Dependencies**: Poetry

## Running the project

### Prerequisites

```bash
poetry install
```

### Tests

```bash
poetry run python -m tests.data
poetry run python -m tests.cli
# All tests
poetry run python -m tests
```

### CLI

```bash
poetry run python -m cli
```

### API + Frontend

```bash
poetry run flask --app api/main.py run
```
