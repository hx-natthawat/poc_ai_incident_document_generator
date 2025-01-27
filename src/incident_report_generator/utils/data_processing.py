"""Data processing utilities for incident reports."""
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging
import pandas as pd

# Configure logging
logger = logging.getLogger(__name__)

def calculate_metrics(df: pd.DataFrame) -> Dict:
    """Calculate key metrics from incident data.
    
    Args:
        df: DataFrame containing incident data
        
    Returns:
        Dictionary containing calculated metrics
    """
    try:
        total_incidents = len(df)
        resolved = len(df[df['Status'] == 'Resolved'])
        resolution_rate = (resolved / total_incidents * 100) if total_incidents > 0 else 0
        
        # Calculate average resolution time for resolved incidents
        resolved_df = df[df['Status'] == 'Resolved'].copy()
        if len(resolved_df) > 0:
            resolved_df['Resolution_Time'] = (
                resolved_df['Resolution_Date'] - resolved_df['Created_Date']
            ).dt.total_seconds() / 3600  # Convert to hours
            avg_resolution_time = resolved_df['Resolution_Time'].mean()
        else:
            avg_resolution_time = 0
        
        # Calculate SLA compliance
        sla_compliant = len(df[df['SLA_Status'] == 'Within SLA'])
        sla_compliance_rate = (sla_compliant / total_incidents * 100) if total_incidents > 0 else 0
        
        metrics = {
            'total_incidents': total_incidents,
            'resolved_incidents': resolved,
            'resolution_rate': resolution_rate,
            'avg_resolution_time': avg_resolution_time,
            'sla_compliance_rate': sla_compliance_rate
        }
        
        logger.info("Successfully calculated incident metrics")
        return metrics
        
    except Exception as e:
        logger.error(f"Error calculating metrics: {str(e)}")
        raise RuntimeError(f"Failed to calculate metrics: {str(e)}")

def analyze_departments(df: pd.DataFrame) -> str:
    """Analyze incident distribution across departments.
    
    Args:
        df: DataFrame containing incident data
        
    Returns:
        Markdown formatted department analysis
    """
    try:
        dept_counts = df['Department'].value_counts()
        dept_resolved = df[df['Status'] == 'Resolved'].groupby('Department').size()
        
        analysis = []
        for dept in dept_counts.index:
            total = dept_counts[dept]
            resolved = dept_resolved.get(dept, 0)
            resolution_rate = (resolved / total * 100) if total > 0 else 0
            
            analysis.append(
                f"### {dept}\n"
                f"- Total Incidents: {total}\n"
                f"- Resolved: {resolved}\n"
                f"- Resolution Rate: {resolution_rate:.1f}%\n"
            )
        
        return "\n".join(analysis)
        
    except Exception as e:
        logger.error(f"Error analyzing departments: {str(e)}")
        raise RuntimeError(f"Failed to analyze departments: {str(e)}")

def analyze_categories(df: pd.DataFrame) -> str:
    """Analyze incident distribution across categories.
    
    Args:
        df: DataFrame containing incident data
        
    Returns:
        Markdown formatted category analysis
    """
    try:
        cat_counts = df['Category'].value_counts()
        cat_priority = df.groupby(['Category', 'Priority']).size().unstack(fill_value=0)
        cat_sla = df.groupby(['Category', 'SLA_Status']).size().unstack(fill_value=0)
        
        analysis = []
        for cat in cat_counts.index:
            total = cat_counts[cat]
            priorities = cat_priority.loc[cat].to_dict()
            sla_status = cat_sla.loc[cat].to_dict()
            
            analysis.append(
                f"### {cat}\n"
                f"- Total Incidents: {total}\n"
                f"- Priority Distribution:\n"
                f"  - High: {priorities.get('High', 0)}\n"
                f"  - Medium: {priorities.get('Medium', 0)}\n"
                f"  - Low: {priorities.get('Low', 0)}\n"
                f"- SLA Status:\n"
                f"  - Within SLA: {sla_status.get('Within SLA', 0)}\n"
                f"  - Breached: {sla_status.get('Breached', 0)}\n"
            )
        
        return "\n".join(analysis)
        
    except Exception as e:
        logger.error(f"Error analyzing categories: {str(e)}")
        raise RuntimeError(f"Failed to analyze categories: {str(e)}")
