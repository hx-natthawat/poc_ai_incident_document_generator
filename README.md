# AI-Powered Incident Report Generator

An automated system for generating detailed incident reports with AI-powered summaries.

## Features

- Generate incident reports from JSON data
- AI-powered Thai language summaries
- PDF report generation with proper formatting
- RESTful API with API key authentication
- Detailed metrics and breakdowns
- Support for Thai language
- Configurable report templates
- SLA compliance tracking
- Department and category analysis
- Interactive API documentation (Swagger UI and ReDoc)

## Project Structure

```
incident_report_generator/
├── data/                      # Sample data and CSV files
│   ├── incident_data.csv
│   └── sample_data.json
├── docs/                      # Documentation
│   └── api.md                # API documentation
├── reports/                   # Generated reports (MD and PDF)
├── src/                      # Source code
│   └── incident_report_generator/
│       ├── __init__.py
│       ├── api.py            # FastAPI service
│       ├── models.py         # Data models
│       ├── report_generator.py # Main report generation logic
│       └── utils/
│           ├── __init__.py
│           ├── ai_integration.py  # OpenAI integration
│           ├── data_processing.py # Data analysis utilities
│           └── pdf_converter.py   # PDF conversion utilities
├── templates/                 # Report templates
│   ├── assets/
│   │   └── logo.svg
│   └── report_template.md
├── tests/                    # Test files
├── .env                      # Environment variables
├── .env.example              # Example environment configuration
├── .gitignore
├── README.md
├── requirements.txt          # Project dependencies
├── run_api.py               # API server script
└── setup.py                 # Package setup file
```

## Setup

### Local Development

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Install wkhtmltopdf (required for PDF generation):

```bash
# macOS
brew install wkhtmltopdf
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env and add your configuration:
# - OPENAI_API_KEY: Your OpenAI API key
# - WKHTMLTOPDF_PATH: Path to wkhtmltopdf binary
# - API_HOST: API host (default: 0.0.0.0)
# - API_PORT: API port (default: 8080)
# - DEBUG: Enable debug mode (default: False)
# - API_KEY: Your secure API key for authentication
```

### Docker Deployment

1. Build and run with Docker Compose:

```bash
# Copy environment file
cp .env.example .env
# Edit .env with your OpenAI API key and API key

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f
```

2. Stop the service:

```bash
docker-compose down
```

## Usage

### Running the API Server

```bash
# Local development
python run_api.py

# Docker
docker-compose up -d
```

The API will be available at:

- API Documentation (Swagger UI): http://localhost:8080/docs
- ReDoc Documentation: http://localhost:8080/redoc

### API Authentication

All API endpoints require authentication using an API key. Include your API key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8080/sample-data
```

### API Endpoints

1. Generate Report (POST `/generate-report`):

```bash
curl -X POST http://localhost:8080/generate-report \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d @data/sample_data.json \
  --output report.pdf
```

2. Get Sample Data (GET `/sample-data`):

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8080/sample-data > sample.json
```

## Report Features

The generated reports include:

- Overall incident statistics
- SLA compliance metrics
- Priority-based analysis
- Department breakdown
- Category analysis
- Resolution time metrics
- Thai language summary
- Detailed incident list

## Development

1. Install development dependencies:

```bash
pip install -e ".[dev]"
```

2. Run tests:

```bash
python test_api.py
```

## Security

- All API endpoints are protected with API key authentication
- API keys should be kept secure and not shared
- Use HTTPS in production
- Follow security best practices when deploying
- Keep dependencies updated

## API Documentation

Detailed API documentation is available in [docs/api.md](docs/api.md) and through the interactive Swagger UI and ReDoc interfaces.
