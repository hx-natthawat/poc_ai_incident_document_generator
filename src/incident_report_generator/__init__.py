"""Incident Report Generator package."""
from .report_generator import IncidentReportGenerator
from .api import app

__version__ = "1.0.0"
__all__ = ["IncidentReportGenerator", "app"]
