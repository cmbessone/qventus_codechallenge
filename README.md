# Parts API

![CI](https://github.com/montevideolabs/parts_api/actions/workflows/ci.yml/badge.svg)

FastAPI  project for Parts Management with SQLAlchemy and Pydantic.
## Prerequisites

- Python 3.13 installed
- Poetry installed (dependency manager)

You can install Poetry easily with:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Installation

Clone the project and follow the steps:

```bash
poetry install
```

Run tests:
```bash
poetry run pytest
```

Preload Test Data:
```bash
poetry run python -m scripts.preload_data
```

Run the API Locally
```bash
poetry run uvicorn app.main:app --reload
```
## Technology Stack

- FastAPI (Web Framework)

- SQLAlchemy (ORM)

- Pydantic (Validations)

- Pytest (Testing)

- Poetry (Dependency Manager)