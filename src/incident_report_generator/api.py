"""FastAPI service for incident report generation."""
import os
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
import logging
import secrets
import time

from fastapi import FastAPI, HTTPException, Security, Depends, Query, Request, Response
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.status import HTTP_403_FORBIDDEN, HTTP_429_TOO_MANY_REQUESTS
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)

# Security setup
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# API Key setup with enhanced security
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY", "your-api-key-here")
if API_KEY == "your-api-key-here":
    logger.warning("Using default API key! Please set a secure API key in environment variables.")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def log_request(request: Request):
    """Log request details."""
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"Client: {request.client.host} "
        f"User-Agent: {request.headers.get('user-agent')}"
    )

def verify_api_key(key: str) -> bool:
    """Verify API key using constant-time comparison."""
    return secrets.compare_digest(key, API_KEY)

async def get_api_key(
    request: Request,
    response: Response,
    api_key_header: str = Security(api_key_header)
):
    """Validate API key with rate limiting and logging."""
    log_request(request)
    
    if not api_key_header or not verify_api_key(api_key_header):
        logger.warning(f"Invalid API key attempt from {request.client.host}")
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return api_key_header

def create_access_token(data: dict):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

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

class ReportInfo(BaseModel):
    """Report information model."""
    filename: str
    created_at: datetime
    file_size: int
    path: str

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "filename": "incident_report_20250127_235959.pdf",
                "created_at": "2025-01-27T23:59:59",
                "file_size": 1024567,
                "path": "/reports/incident_report_20250127_235959.pdf"
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
    Rate limiting is enforced to prevent abuse.
    """,
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# Add rate limit handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

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
@limiter.limit("10/minute")
async def get_sample_data(
    request: Request,
    response: Response,
    api_key: APIKey = Depends(get_api_key)
):
    """
    Get sample incident data in JSON format.
    
    Returns a sample dataset that can be used to test the report generation endpoint.
    Rate limited to 10 requests per minute.
    """
    try:
        sample_file = Path(__file__).parent.parent.parent / "data" / "sample_data.json"
        with open(sample_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading sample data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error loading sample data: {str(e)}")

@app.post("/generate-report", tags=["Reports"])
@limiter.limit("5/minute")
async def generate_report(
    request: Request,
    response: Response,
    data: IncidentData,
    api_key: APIKey = Depends(get_api_key)
):
    """
    Generate a PDF report from incident data.
    
    Takes a list of incidents and generates a detailed PDF report.
    Rate limited to 5 requests per minute due to resource intensity.
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
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/reports/list", tags=["Reports"])
@limiter.limit("20/minute")
async def list_reports(
    request: Request,
    response: Response,
    limit: int = Query(10, description="Maximum number of reports to return"),
    skip: int = Query(0, description="Number of reports to skip"),
    api_key: APIKey = Depends(get_api_key)
):
    """
    List available incident reports.
    
    Returns a list of report information including filename, creation date, and file size.
    Rate limited to 20 requests per minute.
    """
    try:
        reports_dir = Path("/app/reports")
        reports = []
        
        for report in sorted(reports_dir.glob("*.pdf"), key=lambda x: x.stat().st_mtime, reverse=True):
            stat = report.stat()
            reports.append(
                ReportInfo(
                    filename=report.name,
                    created_at=datetime.fromtimestamp(stat.st_mtime),
                    file_size=stat.st_size,
                    path=str(report)
                )
            )
        
        # Apply pagination
        total = len(reports)
        reports = reports[skip:skip + limit]
        
        return {
            "total": total,
            "reports": reports,
            "limit": limit,
            "skip": skip
        }
        
    except Exception as e:
        logger.error(f"Error listing reports: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing reports: {str(e)}")

@app.get("/reports/latest", tags=["Reports"])
@limiter.limit("10/minute")
async def get_latest_report(
    request: Request,
    response: Response,
    api_key: APIKey = Depends(get_api_key)
):
    """
    Get the most recently generated incident report.
    
    Returns the PDF file of the latest report.
    Rate limited to 10 requests per minute.
    """
    try:
        reports_dir = Path("reports")
        if not reports_dir.exists():
            raise HTTPException(
                status_code=404,
                detail="No reports directory found"
            )
        
        # Get the most recent PDF file
        pdf_files = sorted(
            reports_dir.glob("*.pdf"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if not pdf_files:
            raise HTTPException(
                status_code=404,
                detail="No reports found"
            )
        
        latest_report = pdf_files[0]
        return FileResponse(
            path=latest_report,
            filename=latest_report.name,
            media_type='application/pdf'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving latest report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving latest report: {str(e)}"
        )

@app.get("/reports/download/{filename}", tags=["Reports"])
@limiter.limit("30/minute")
async def download_report(
    request: Request,
    response: Response,
    filename: str,
    api_key: APIKey = Depends(get_api_key)
):
    """
    Download a specific report by filename.
    
    Returns the PDF file for download.
    Rate limited to 30 requests per minute.
    """
    try:
        reports_dir = Path("/app/reports")
        file_path = reports_dir / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Report not found")
            
        if not filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Invalid file type")
            
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/pdf'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading report: {str(e)}")

@app.get("/health", tags=["System"])
@limiter.limit("60/minute")
async def health_check(
    request: Request,
    response: Response,
    api_key: APIKey = Depends(get_api_key)
):
    """
    Health check endpoint for monitoring system status.
    Returns system health information including:
    - API status
    - Dependencies status
    - Storage status
    - Memory usage
    Rate limited to 60 requests per minute.
    """
    try:
        # Check storage
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        storage_ok = reports_dir.exists() and os.access(reports_dir, os.W_OK)
        
        # Check wkhtmltopdf
        wkhtmltopdf_path = os.getenv("WKHTMLTOPDF_PATH", "wkhtmltopdf")
        try:
            import subprocess
            result = subprocess.run([wkhtmltopdf_path, "--version"], 
                                 capture_output=True, 
                                 text=True)
            wkhtmltopdf_ok = result.returncode == 0
            wkhtmltopdf_version = result.stdout.strip() if wkhtmltopdf_ok else None
        except Exception:
            wkhtmltopdf_ok = False
            wkhtmltopdf_version = None
        
        # Check OpenAI API
        openai_key = os.getenv("OPENAI_API_KEY")
        openai_ok = bool(openai_key and len(openai_key) > 20)
        
        # Get system memory info
        import psutil
        memory = psutil.virtual_memory()
        memory_info = {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used
        }
        
        # Check disk space
        disk = psutil.disk_usage(".")
        disk_info = {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
        
        status = {
            "status": "healthy" if all([storage_ok, wkhtmltopdf_ok, openai_ok]) else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "dependencies": {
                "storage": {
                    "status": "ok" if storage_ok else "error",
                    "reports_dir": str(reports_dir.absolute())
                },
                "wkhtmltopdf": {
                    "status": "ok" if wkhtmltopdf_ok else "error",
                    "version": wkhtmltopdf_version
                },
                "openai": {
                    "status": "ok" if openai_ok else "error"
                }
            },
            "system": {
                "memory": memory_info,
                "disk": disk_info
            }
        }
        
        response_code = 200 if status["status"] == "healthy" else 503
        response.status_code = response_code
        
        return status
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )

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
            "POST /generate-report": "Generate a PDF report from incident data",
            "GET /reports": "List available incident reports",
            "GET /reports/latest": "Get the most recently generated incident report",
            "GET /health": "Health check endpoint for monitoring system status"
        }
    }
