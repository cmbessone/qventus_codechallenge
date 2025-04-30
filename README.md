# Parts API

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

3. Run the development server:
```bash
poetry run uvicorn app.main:app --reload
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
- Performs code quality checks (black, flake8)
- Runs tests
- Verifies application build