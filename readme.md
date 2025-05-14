# Recipe Bot MCP

A Model Context Protocol (MCP) implementation that helps users find recipes based on their available ingredients and dietary restrictions.

## Project Structure

```
recipe_bot/
├── src/                    # Source code
│   ├── api/               # API endpoints
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── docs/                  # Documentation
├── config/                # Configuration files
└── requirements.txt       # Project dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up pre-commit hooks:
```bash
pre-commit install
```

## Development

- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8`

## License

MIT
