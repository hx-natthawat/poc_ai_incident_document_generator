# Incident Report Generator

An AI-powered incident report generator that creates detailed PDF reports from incident data. Built with FastAPI and OpenAI.

## Features

- Generate comprehensive PDF reports from incident data
- AI-powered incident analysis and summaries
- Department and category breakdowns
- SLA compliance tracking
- Priority-based metrics
- Modern REST API with API key authentication
- Report management (list, retrieve latest)
- Customizable PDF styling with CSS

## Security Features

- Rate limiting on all endpoints
- Comprehensive request logging
- Security headers (HSTS, XSS Protection)
- API key rotation system
- JWT token support
- Secure key validation
- Environment variable security

## Prerequisites

- Python 3.8+
- wkhtmltopdf (for PDF generation)
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/incident-report-generator.git
cd incident-report-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install wkhtmltopdf:
- macOS: `brew install wkhtmltopdf`
- Linux: `apt-get install wkhtmltopdf`
- Windows: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration:
# Required variables:
# - OPENAI_API_KEY: Your OpenAI API key
# - API_KEY: Your secure API key for authentication
# - SECRET_KEY: Your secure secret key for JWT
# Optional variables:
# - WKHTMLTOPDF_PATH: Path to wkhtmltopdf binary
# - API_HOST: API host (default: 0.0.0.0)
# - API_PORT: API port (default: 8000)
# - DEBUG: Enable debug mode (default: False)
```

## Usage

1. Start the API server:
```bash
python run_api.py
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Data Management
- `GET /sample-data` - Get sample incident data (10 requests/minute)
- `POST /generate-report` - Generate a PDF report from incident data (5 requests/minute)

### Report Management
- `GET /reports` - List available reports with pagination (20 requests/minute)
- `GET /reports/latest` - Get the most recent report (10 requests/minute)
- `GET /` - API information and available endpoints

### Authentication

All endpoints require an API key passed in the `X-API-Key` header. The API implements:
- API key rotation with expiration
- Secure key validation using constant-time comparison
- Rate limiting to prevent abuse
- Request logging and monitoring

## Testing

Run the test suite:
```bash
python test_api.py
```

## Project Structure

```
incident-report-generator/
├── data/                    # Sample data and resources
├── reports/                 # Generated reports
├── src/
│   └── incident_report_generator/
│       ├── api.py          # FastAPI application
│       ├── report_generator.py  # Report generation logic
│       └── utils/
│           ├── ai_integration.py    # OpenAI integration
│           ├── data_processing.py   # Data analysis
│           ├── key_management.py    # API key rotation
│           └── pdf_converter.py     # PDF generation
├── tests/                  # Test files
├── .env.example           # Example environment variables
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
