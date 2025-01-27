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

- Python 3.8+ or Docker
- wkhtmltopdf (for PDF generation, not needed with Docker)
- OpenAI API key

## Installation

### Local Development

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

### Docker Deployment

1. Build and run with Docker Compose:
```bash
# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Start the service
docker compose up -d

# View logs
docker compose logs -f api

# Stop the service
docker compose down
```

## Production Deployment

1. Set up SSL certificates:
```bash
mkdir -p nginx/ssl
# Generate self-signed certificates (for testing only)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -subj "/CN=localhost"
```

2. Create production environment file:
```bash
cp .env.prod.example .env.prod
```

3. Update production environment variables in `.env.prod`:
```
PORT=8081
OPENAI_API_KEY=your_openai_api_key
API_KEY=your_api_key
DEBUG=0
ENVIRONMENT=production
LOG_LEVEL=INFO
```

4. Start the production stack:
```bash
docker compose -f docker-compose.prod.yml up -d
```

The production setup includes:
- Multiple API instances for high availability
- Nginx as a reverse proxy and load balancer
- HTTPS support
- Health monitoring
- Resource limits and logging

## Usage

### Local Development
```bash
python run_api.py
```

### Docker
```bash
docker compose up -d
```

Access the API documentation:
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
# Local testing
python test_api.py

# Docker testing
docker compose exec api python test_api.py
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
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile            # Docker build configuration
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
