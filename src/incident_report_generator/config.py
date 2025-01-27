"""Configuration settings for the incident report generator."""
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
REPORTS_DIR = BASE_DIR / "reports"

# Data files
INCIDENT_DATA_FILE = DATA_DIR / "incident_data.csv"
REPORT_TEMPLATE_FILE = TEMPLATES_DIR / "report_template.md"

# OpenAI settings
DEFAULT_MODEL = "gpt-4"
MAX_TOKENS = 500
TEMPERATURE = 0.7

# Report settings
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
PDF_PAGE_SIZE = "A4"
PDF_MARGINS = {
    "top": "25mm",
    "right": "25mm",
    "bottom": "25mm",
    "left": "25mm"
}

# Technical terms to preserve in Thai translation
TECHNICAL_TERMS = [
    "SLA",
    "High",
    "Medium",
    "Low",
    "Resolved",
    "Unresolved",
    "Priority",
    "Status",
    "ID"
]
