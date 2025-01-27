# Quick Start Guide

This guide will help you get started with the Incident Report Generator API quickly.

## Prerequisites

1. API Key - You'll need a valid API key to access the endpoints
2. HTTP Client (curl, Postman, or any programming language)
3. For development: Docker and Docker Compose

## Development Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd incident-report-generator
```

2. Create environment file:

```bash
cp .env.example .env
# Edit .env with your settings
```

3. Start the development server:

```bash
docker compose up -d
```

4. Test the API:

```bash
python test_api_dev.py
```

## Production Setup

1. Set up SSL certificates:

```bash
mkdir -p nginx/ssl
# Add your SSL certificates:
# - nginx/ssl/cert.pem
# - nginx/ssl/key.pem
```

2. Create production environment file:

```bash
cp .env.prod.example .env.prod
# Edit .env.prod with your production settings
```

3. Start the production server:

```bash
docker compose -f docker-compose.prod.yml up -d
```

4. Test the production API:

```bash
python test_api_prod.py
```

## Basic Usage Examples

### 1. Generate a Report

```bash
curl -k -H "X-API-Key: your-api-key" \
     -H "Content-Type: application/json" \
     -d '{
       "incidents": [{
         "ID": "INC001",
         "Title": "Test Incident",
         "Description": "Test description",
         "Status": "Open",
         "Priority": "High",
         "Department": "IT",
         "Category": "Infrastructure",
         "Created_Date": "2025-01-27T10:00:00",
         "Resolution_Date": null,
         "SLA_Status": "Within SLA"
       }]
     }' \
     https://localhost/generate-report \
     --output report.pdf
```

### 2. List Available Reports

```bash
curl -k -H "X-API-Key: your-api-key" \
     https://localhost/reports/list
```

### 3. Download Latest Report

```bash
curl -k -H "X-API-Key: your-api-key" \
     https://localhost/reports/latest \
     --output latest_report.pdf
```

## Using Postman

1. Import the Postman collection from `docs/postman_collection.json`
2. Create an environment with variables:
   - `base_url`: `http://localhost:8080` (dev) or `https://your-domain` (prod)
   - `api_key`: Your API key
3. Select the imported collection and environment
4. Start making requests!

## Rate Limits

Be aware of the rate limits for each endpoint:

- Generate Report: 5 requests/minute
- List Reports: 20 requests/minute
- Download Report: 30 requests/minute
- Latest Report: 10 requests/minute
- Sample Data: 10 requests/minute
- Health Check: 60 requests/minute

## Common Issues

1. **Connection Refused**

   - Check if the API server is running
   - Verify the correct port (8080 for dev, 443 for prod)

2. **Invalid API Key**

   - Ensure the API key is correctly set in the X-API-Key header
   - Check if the API key matches the one in your .env file

3. **SSL Certificate Errors**

   - Development: Use `-k` flag with curl or disable SSL verification
   - Production: Ensure valid SSL certificates are installed

4. **Rate Limit Exceeded**
   - Wait for the rate limit window to reset
   - Consider implementing request queuing in your client

## Next Steps

1. Review the full [API Documentation](api.md)
2. Explore the report template customization options
3. Set up monitoring and logging
4. Implement proper error handling in your client

## Support

If you encounter any issues:

1. Check the [API Documentation](api.md)
2. Review the error messages and logs
3. Contact the development team
4. Submit issues through the project repository
