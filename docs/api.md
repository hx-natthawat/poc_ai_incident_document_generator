# Incident Report Generator API Documentation

## Overview

The Incident Report Generator API provides endpoints for generating detailed incident reports with AI-powered summaries. The API uses API key authentication for security and provides comprehensive documentation through Swagger UI and ReDoc interfaces.

## Base URLs

- Local Development: `http://localhost:8080`
- Docker: `http://localhost:8080`

For production deployments, configure the host and port through environment variables:
- `API_HOST`: Host address (default: 0.0.0.0)
- `API_PORT`: Port number (default: 8080)

## Authentication

All API endpoints require authentication using an API key. The API key must be included in the `X-API-Key` header with every request:

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8080/endpoint
```

To configure your API key:
1. Copy `.env.example` to `.env`
2. Set your secure API key:
   ```
   API_KEY=your-secure-api-key
   ```

### Security Best Practices

1. Use strong, randomly generated API keys
2. Keep API keys secure and never commit them to version control
3. Use HTTPS in production environments
4. Rotate API keys regularly
5. Monitor API usage for suspicious activity

## API Documentation Interfaces

1. **Swagger UI**
   - URL: `/docs`
   - Features:
     - Interactive API testing
     - Request/response examples
     - Authentication documentation
     - Schema information

2. **ReDoc**
   - URL: `/redoc`
   - Features:
     - Clean, responsive interface
     - Search functionality
     - Schema documentation
     - Security requirements

3. **OpenAPI Schema**
   - URL: `/openapi.json`
   - Raw OpenAPI specification

## Endpoints

### 1. Root Endpoint

```http
GET /
```

Returns information about the API and available endpoints.

**Authentication:**
- Required: Yes
- Header: `X-API-Key`

**Response Example:**
```json
{
  "name": "Incident Report Generator API",
  "version": "1.0.0",
  "endpoints": [
    {"path": "/", "method": "GET", "description": "This information"},
    {"path": "/sample-data", "method": "GET", "description": "Get sample incident data"},
    {"path": "/generate-report", "method": "POST", "description": "Generate PDF report from incident data"},
    {"path": "/docs", "method": "GET", "description": "API documentation (Swagger UI)"},
    {"path": "/redoc", "method": "GET", "description": "API documentation (ReDoc)"}
  ]
}
```

### 2. Get Sample Data

```http
GET /sample-data
```

Returns sample incident data that can be used to test the report generation endpoint.

**Authentication:**
- Required: Yes
- Header: `X-API-Key`

**Response:**
- Content-Type: `application/json`

**Response Example:**
```json
{
  "incidents": [
    {
      "Incident_ID": "INC001",
      "Title": "System Outage",
      "Priority": "High",
      "Department": "IT",
      "Category": "Infrastructure",
      "Status": "Resolved",
      "Created_On": "2025-01-27T10:00:00",
      "Resolved_On": "2025-01-27T12:00:00",
      "SLA_Status": "Within SLA"
    }
  ]
}
```

### 3. Generate Report

```http
POST /generate-report
```

Generates a PDF report from the provided incident data.

**Authentication:**
- Required: Yes
- Header: `X-API-Key`

**Request Headers:**
- Content-Type: `application/json`
- X-API-Key: `your-api-key`

**Request Body:**
```json
{
  "incidents": [
    {
      "Incident_ID": "INC001",
      "Title": "System Outage",
      "Priority": "High",
      "Department": "IT",
      "Category": "Infrastructure",
      "Status": "Resolved",
      "Created_On": "2025-01-27T10:00:00",
      "Resolved_On": "2025-01-27T12:00:00",
      "SLA_Status": "Within SLA"
    }
  ]
}
```

**Response:**
- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename=incident_report_YYYYMMDD_HHMMSS.pdf`

The response will be a PDF file containing the generated report with:
- Overall incident statistics
- SLA compliance metrics
- Priority-based analysis
- Department breakdown
- Category analysis
- Resolution time metrics
- AI-powered summary
- Detailed incident list

## Error Handling

The API uses standard HTTP status codes:

| Status Code | Description |
|------------|-------------|
| 200 | Success |
| 403 | Invalid or missing API key |
| 422 | Invalid request data |
| 500 | Server error |

Error responses include a JSON body with details:

```json
{
  "detail": "Error message description"
}
```

## Rate Limiting

The API currently does not implement rate limiting, but users should:
1. Implement appropriate retry mechanisms
2. Handle errors gracefully
3. Monitor API usage
4. Contact support if high-volume usage is needed

## Development and Testing

1. Test the API using the provided sample data:
   ```bash
   curl -H "X-API-Key: your-api-key" http://localhost:8080/sample-data > test_data.json
   curl -X POST http://localhost:8080/generate-report \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-api-key" \
     -d @test_data.json \
     --output report.pdf
   ```

2. Run the test script:
   ```bash
   python test_api.py
   ```

## Support

For issues, questions, or feature requests:
1. Check the API documentation
2. Review error messages and logs
3. Submit an issue in the repository
4. Contact the development team

## API Versioning

The current API version is 1.0.0. Future versions will maintain backward compatibility where possible, and breaking changes will be communicated through the API version number.
