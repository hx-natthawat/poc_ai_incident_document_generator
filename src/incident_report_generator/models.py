"""Data models for the incident report generator."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Incident(BaseModel):
    """Model for a single incident."""
    Incident_ID: str = Field(..., description="Unique identifier for the incident")
    Title: str = Field(..., description="Title of the incident")
    Priority: str = Field(..., description="Priority level (High, Medium, Low)")
    Department: str = Field(..., description="Department responsible")
    Category: str = Field(..., description="Incident category")
    Status: str = Field(..., description="Current status (Resolved, Unresolved)")
    Created_On: datetime = Field(..., description="Creation timestamp")
    Resolved_On: Optional[datetime] = Field(None, description="Resolution timestamp")
    SLA_Status: str = Field(..., description="SLA status (Within SLA, SLA Breached)")

class IncidentData(BaseModel):
    """Model for incident data input."""
    incidents: List[Incident]
