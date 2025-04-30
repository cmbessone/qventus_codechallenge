# Parts API

[![CI](https://github.com/cmbessone/qventus_codechallenge/actions/workflows/ci.yml/badge.svg)](https://github.com/cmbessone/qventus_codechallenge/actions/workflows/ci.yml)


A FastAPI service for managing parts inventory with SQLite database.

## Requirements

- Python 3.11
- Poetry (Python package manager)

## Setup

1. Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Activate the virtual environment
```bash
poetry shell
```

4. Run the development server:
```bash
poetry run uvicorn app.main:app --reload
```

5. Preload sample data:
```bash
poetry run preload-data
```


## Development

- Format code:
```bash
poetry run black .
```

- Run linting:
```bash
poetry run flake8 .
```

- Run tests:
```bash
poetry run pytest
```

## API Documentation

Once the server is running, you can access:
- API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Project Structure

```
.
├── app/                    # Application package
│   ├── models/            # SQLAlchemy models
│   ├── routers/           # FastAPI route handlers
│   ├── schemas/           # Pydantic models
│   ├── services/          # Business logic
│   └── repository/        # Database operations
├── tests/                 # Test files
└── scripts/               # Utility scripts
```

## GitHub Actions

The project uses GitHub Actions for CI/CD:
- Runs on every push to main and pull requests
- Checks code format (Black)
- Performs linting (Flake8)
- Runs tests (Pytest)
- Verifies that the application can boot via uvicorn