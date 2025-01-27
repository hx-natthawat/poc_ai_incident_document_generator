# Incident Report Generator

An API service for generating detailed incident reports with AI-powered summaries.

## Features

- Generate PDF reports from incident data with AI-enhanced summaries
- Secure API access with API key authentication
- Rate limiting to prevent abuse
- Load balancing with multiple API instances
- HTTPS support with SSL/TLS
- Persistent report storage using Docker volumes
- Beautiful report template with company logo

## API Endpoints

### Reports
- `POST /generate-report` - Generate a new incident report (Rate limit: 5/min)
- `GET /reports/list` - List available reports with pagination (Rate limit: 20/min)
- `GET /reports/download/{filename}` - Download a specific report (Rate limit: 30/min)
- `GET /reports/latest` - Get the most recent report (Rate limit: 10/min)

### Utilities
- `GET /sample-data` - Get sample incident data (Rate limit: 10/min)
- `GET /health` - Check API health status (Rate limit: 60/min)

## Development Setup

1. Clone the repository
2. Create a `.env` file based on `.env.example`
3. Run development server:
```bash
docker compose up -d
```

4. Test the development API:
```bash
python test_api_dev.py
```

## Production Deployment

1. Create `.env.prod` based on `.env.prod.example`
2. Set up SSL certificates in `nginx/ssl/`
3. Run production server:
```bash
docker compose -f docker-compose.prod.yml up -d
```

4. Test the production API:
```bash
python test_api_prod.py
```

## Environment Variables

### Development
- `API_PORT` - API server port (default: 8080)
- `API_KEY` - API authentication key
- `OPENAI_API_KEY` - OpenAI API key for AI summaries

### Production
Additional variables in `.env.prod`:
- `SSL_CERTIFICATE` - Path to SSL certificate
- `SSL_KEY` - Path to SSL private key
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

## Docker Volumes

- `reports_data` - Persistent storage for generated reports
- `nginx/ssl` - SSL certificates for HTTPS
- `nginx/conf.d` - Nginx configuration
- `data` - Application data directory
- `templates` - Report templates and assets

## Testing

The project includes two test scripts:
- `test_api_dev.py` - Test development environment (HTTP, port 8080)
- `test_api_prod.py` - Test production environment (HTTPS, port 443)

## Report Templates

Reports are generated using a customizable markdown template located at `templates/report_template.md`. The template includes:
- Company logo
- Executive summary with AI-generated insights
- Detailed incident analysis
- Key metrics and statistics
- Department and category breakdowns

## Security

- API key authentication required for all endpoints
- Rate limiting to prevent abuse
- HTTPS encryption in production
- Secure file handling
- Environment variable configuration
- No sensitive data in logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
