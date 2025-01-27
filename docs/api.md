# Incident Report Generator API Documentation

## Overview

The Incident Report Generator API provides endpoints for generating detailed incident reports with AI-powered summaries. The API is secured with API key authentication and provides comprehensive documentation through Swagger UI and ReDoc interfaces.

## Authentication

All API endpoints require authentication using an API key. Include your API key in the `X-API-Key` header with every request:

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8080/endpoint
```

## Base URL

The base URL for all API endpoints is: `http://localhost:8080`

## API Documentation Interfaces

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI Schema: `/openapi.json`

## Endpoints

### 1. Get API Information

```
GET /
```

Returns information about the API and available endpoints.

**Headers:**

- `X-API-Key`: Your API key (required)

**Response:**

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
    }
  ]
}
```

### 2. Get Sample Data

```
GET /sample-data
```

Returns sample incident data that can be used to test the report generation endpoint.

**Headers:**

- `X-API-Key`: Your API key (required)

**Response:**

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

```
POST /generate-report
```

Generates a PDF report from the provided incident data.

**Headers:**

- `X-API-Key`: Your API key (required)
- `Content-Type`: application/json

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

- Content-Type: application/pdf
- The response will be a PDF file containing the generated report

## Report Features

The generated PDF reports include:

- Overall incident statistics
- SLA compliance metrics
- Priority-based analysis
- Department breakdown
- Category analysis
- Resolution time metrics
- Thai language summary
- Detailed incident list

## Error Responses

The API uses standard HTTP status codes:

- `200 OK`: Request successful
- `403 Forbidden`: Invalid or missing API key
- `422 Unprocessable Entity`: Invalid request data
- `500 Internal Server Error`: Server error

Error responses will include a JSON body with details:

```json
{
  "detail": "Error message here"
}
```

## Rate Limiting

Please be mindful of rate limits and API usage guidelines. Implement appropriate retry mechanisms in your client applications.

## Security Recommendations

1. Keep your API key secure and never share it
2. Use HTTPS in production environments
3. Implement proper error handling in your client applications
4. Monitor API usage for suspicious activity
5. Regularly rotate API keys
6. Keep client libraries and dependencies updated
