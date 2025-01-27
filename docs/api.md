# Incident Report Generator API Documentation

## Overview

The Incident Report Generator API provides endpoints for generating detailed incident reports with AI-powered summaries. The API uses API key authentication for security and implements rate limiting to prevent abuse.

## Base URLs

- Local Development: `http://localhost:8080`
- Docker: `http://localhost:8080`
- Production: `https://your-domain`

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

## Rate Limiting

The API implements rate limiting to ensure fair usage and system stability:

| Endpoint                       | Rate Limit         |
| ------------------------------ | ------------------ |
| `/generate-report`             | 5 requests/minute  |
| `/reports/list`                | 20 requests/minute |
| `/reports/download/{filename}` | 30 requests/minute |
| `/reports/latest`              | 10 requests/minute |
| `/sample-data`                 | 10 requests/minute |
| `/health`                      | 60 requests/minute |

When rate limit is exceeded, the API returns a 429 (Too Many Requests) status code.

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
    { "path": "/", "method": "GET", "description": "This information" },
    {
      "path": "/sample-data",
      "method": "GET",
      "description": "Get sample incident data"
    },
    {
      "path": "/generate-report",
      "method": "POST",
      "description": "Generate PDF report from incident data"
    },
    {
      "path": "/docs",
      "method": "GET",
      "description": "API documentation (Swagger UI)"
    },
    {
      "path": "/redoc",
      "method": "GET",
      "description": "API documentation (ReDoc)"
    },
    {
      "path": "/reports/list",
      "method": "GET",
      "description": "List available reports"
    },
    {
      "path": "/reports/download/{filename}",
      "method": "GET",
      "description": "Download a specific report"
    },
    {
      "path": "/reports/latest",
      "method": "GET",
      "description": "Get the latest report"
    },
    { "path": "/health", "method": "GET", "description": "API health check" }
  ]
}
```

### 2. Get Sample Data

```http
GET /sample-data
```

Returns sample incident data that can be used to test the report generation endpoint.

**Rate Limit:** 10 requests/minute

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
      "ID": "INC001",
      "Title": "System Outage",
      "Description": "Complete system outage affecting all users",
      "Status": "Resolved",
      "Priority": "High",
      "Department": "IT",
      "Category": "Infrastructure",
      "Created_Date": "2025-01-27T10:00:00",
      "Resolution_Date": "2025-01-27T12:00:00",
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

**Rate Limit:** 5 requests/minute

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
      "ID": "INC001",
      "Title": "System Outage",
      "Description": "Complete system outage affecting all users",
      "Status": "Resolved",
      "Priority": "High",
      "Department": "IT",
      "Category": "Infrastructure",
      "Created_Date": "2025-01-27T10:00:00",
      "Resolution_Date": "2025-01-27T12:00:00",
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

### 4. List Reports

```http
GET /reports/list
```

Lists available reports with pagination support.

**Rate Limit:** 20 requests/minute

**Authentication:**

- Required: Yes
- Header: `X-API-Key`

**Query Parameters:**

- `limit` (optional): Maximum number of reports to return (default: 10)
- `skip` (optional): Number of reports to skip (default: 0)

**Response Example:**

```json
{
  "total": 25,
  "reports": [
    {
      "filename": "incident_report_20250127_180617.pdf",
      "created_at": "2025-01-27T18:06:17.628516",
      "file_size": 24234,
      "path": "/app/reports/incident_report_20250127_180617.pdf"
    }
  ],
  "limit": 10,
  "skip": 0
}
```

### 5. Download Report

```http
GET /reports/download/{filename}
```

Downloads a specific report by filename.

**Rate Limit:** 30 requests/minute

**Authentication:**

- Required: Yes
- Header: `X-API-Key`

**Parameters:**

- `filename`: Name of the report file to download

**Response:**

- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename={filename}`

### 6. Get Latest Report

```http
GET /reports/latest
```

Downloads the most recently generated report.

**Rate Limit:** 10 requests/minute

**Authentication:**

- Required: Yes
- Header: `X-API-Key`

**Response:**

- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename={latest_report_name}`

### 7. Health Check

```http
GET /health
```

Returns the API's health status.

**Rate Limit:** 60 requests/minute

**Authentication:**

- Required: Yes
- Header: `X-API-Key`

**Response Example:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-27T18:06:17.628516"
}
```

## Error Handling

The API uses standard HTTP status codes:

| Status Code | Description                             |
| ----------- | --------------------------------------- |
| 200         | Success                                 |
| 400         | Bad Request                             |
| 401         | Unauthorized (Invalid API key)          |
| 404         | Not Found                               |
| 429         | Too Many Requests (Rate limit exceeded) |
| 500         | Internal Server Error                   |

Error responses include a JSON body with details:

```json
{
  "detail": "Error message description"
}
```

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
