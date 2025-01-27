"""Data processing utilities for incident reports."""
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd

def load_incident_data(file_path: Path) -> pd.DataFrame:
    """Load and preprocess incident data from CSV or JSON."""
    if file_path.suffix.lower() == '.csv':
        df = pd.read_csv(file_path)
    else:  # JSON
        df = pd.read_json(file_path)
        if 'incidents' in df.columns:
            df = pd.json_normalize(df['incidents'])
    
    # Convert datetime columns
    for col in ['Created_On', 'Resolved_On']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    
    return df

def calculate_sla_compliance(df: pd.DataFrame) -> Tuple[int, int, int, float]:
    """Calculate SLA compliance metrics.
    
    Returns:
        Tuple containing:
        - Total incidents
        - Number within SLA
        - Number breaching SLA
        - Compliance rate as percentage
    """
    total = len(df)
    within_sla = len(df[df['SLA_Status'] == 'Within SLA'])
    breached_sla = total - within_sla
    compliance_rate = (within_sla / total * 100) if total > 0 else 0
    
    return total, within_sla, breached_sla, compliance_rate

def get_priority_breakdown(df: pd.DataFrame) -> Dict:
    """Calculate incident breakdown by priority level."""
    breakdown = {}
    for priority in df['Priority'].unique():
        priority_df = df[df['Priority'] == priority]
        total = len(priority_df)
        resolved = len(priority_df[priority_df['Status'] == 'Resolved'])
        sla_breached = len(priority_df[priority_df['SLA_Status'] == 'SLA Breached'])
        
        # Calculate average resolution time
        resolved_df = priority_df[priority_df['Status'] == 'Resolved'].copy()
        if not resolved_df.empty:
            resolved_df['resolution_time'] = (
                resolved_df['Resolved_On'] - resolved_df['Created_On']
            ).dt.total_seconds() / 3600  # Convert to hours
            avg_time = resolved_df['resolution_time'].mean()
        else:
            avg_time = 0
        
        breakdown[priority] = {
            'total': total,
            'resolved': resolved,
            'unresolved': total - resolved,
            'sla_breached': sla_breached,
            'compliance_rate': ((total - sla_breached) / total * 100) if total > 0 else 0,
            'avg_resolution_time': avg_time
        }
    
    return breakdown

def get_department_breakdown(df: pd.DataFrame) -> Dict:
    """Calculate incident breakdown by department."""
    breakdown = {}
    for dept in df['Department'].unique():
        dept_df = df[df['Department'] == dept]
        total = len(dept_df)
        within_sla = len(dept_df[dept_df['SLA_Status'] == 'Within SLA'])
        breached = total - within_sla
        compliance_rate = (within_sla / total * 100) if total > 0 else 0
        
        breakdown[dept] = (total, within_sla, breached, compliance_rate)
    
    return breakdown

def get_category_breakdown(df: pd.DataFrame) -> Dict:
    """Calculate incident breakdown by category."""
    breakdown = {}
    for cat in df['Category'].unique():
        cat_df = df[df['Category'] == cat]
        total = len(cat_df)
        within_sla = len(cat_df[cat_df['SLA_Status'] == 'Within SLA'])
        breached = total - within_sla
        compliance_rate = (within_sla / total * 100) if total > 0 else 0
        
        breakdown[cat] = (total, within_sla, breached, compliance_rate)
    
    return breakdown
