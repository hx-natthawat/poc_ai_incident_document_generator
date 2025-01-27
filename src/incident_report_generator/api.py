"""FastAPI service for incident report generation."""
import json
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.status import HTTP_403_FORBIDDEN
from pydantic import BaseModel

# API Key setup
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY", "your-api-key-here")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if not api_key_header or api_key_header != API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )
    return api_key_header

class Incident(BaseModel):
    """Incident data model."""
    ID: str
    Title: str
    Description: str
    Status: str
    Priority: str
    Department: str
    Category: str
    Created_Date: datetime
    Resolution_Date: Optional[datetime] = None
    SLA_Status: str

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
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
        }

class IncidentData(BaseModel):
    """Collection of incidents."""
    incidents: List[Incident]

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
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
        }

app = FastAPI(
    title="Incident Report Generator API",
    description="""
    Generate detailed incident reports with AI-powered summaries.
    
    Features:
    * Generate PDF reports from incident data
    * AI-powered incident analysis
    * Department and category breakdowns
    * SLA compliance tracking
    * Priority-based metrics
    
    All endpoints require API key authentication via the X-API-Key header.
    """,
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI with security information."""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Incident Report Generator API - Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """ReDoc API documentation."""
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Incident Report Generator API - ReDoc</title>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
            <style>body { margin: 0; padding: 0; }</style>
        </head>
        <body>
            <redoc spec-url="/openapi.json"></redoc>
            <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"></script>
        </body>
        </html>
        """
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    """Return OpenAPI schema."""
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

@app.get("/sample-data", tags=["Data"])
async def get_sample_data(api_key: APIKey = Depends(get_api_key)):
    """
    Get sample incident data in JSON format.
    
    Returns a sample dataset that can be used to test the report generation endpoint.
    """
    try:
        sample_file = Path(__file__).parent.parent.parent / "data" / "sample_data.json"
        with open(sample_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading sample data: {str(e)}")

@app.post("/generate-report", tags=["Reports"])
async def generate_report(data: IncidentData, api_key: APIKey = Depends(get_api_key)):
    """
    Generate a PDF report from incident data.
    
    Takes a list of incidents and generates a detailed PDF report with:
    * Overall incident statistics
    * SLA compliance metrics
    * Priority-based analysis
    * Department breakdown
    * Category analysis
    * AI-powered summary
    * Detailed incident list
    
    Returns the generated PDF file.
    """
    try:
        from .report_generator import IncidentReportGenerator
        
        # Initialize report generator
        generator = IncidentReportGenerator()
        
        # Convert pydantic model to dict and extract incidents list
        incidents = [incident.dict() for incident in data.incidents]
        
        # Generate report
        report_path = generator.generate_report(incidents)
        
        # Return the PDF file
        return FileResponse(
            path=report_path,
            filename=report_path.name,
            media_type='application/pdf'
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/", tags=["Info"])
async def root(api_key: APIKey = Depends(get_api_key)):
    """Get API information and available endpoints."""
    return {
        "name": "Incident Report Generator API",
        "version": "1.0.0",
        "description": "Generate detailed incident reports with AI-powered summaries",
        "endpoints": {
            "GET /": "This information",
            "GET /docs": "Interactive API documentation (Swagger UI)",
            "GET /redoc": "Alternative API documentation (ReDoc)",
            "GET /sample-data": "Get sample incident data",
            "POST /generate-report": "Generate a PDF report from incident data"
        }
    }
