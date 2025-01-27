"""Incident report generator module."""
import os
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import logging
from typing import Dict, List, Optional, Union

from .utils.data_processing import calculate_metrics, analyze_departments, analyze_categories
from .utils.ai_integration import generate_summary
from .utils.pdf_converter import markdown_to_pdf

# Configure logging
logger = logging.getLogger(__name__)

class IncidentReportGenerator:
    """Class for generating incident reports."""
    
    def __init__(self, output_dir: Union[str, Path] = "reports"):
        """Initialize the report generator.
        
        Args:
            output_dir: Directory to save generated reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def json_to_dataframe(self, json_data: List[Dict]) -> pd.DataFrame:
        """Convert JSON data to pandas DataFrame.
        
        Args:
            json_data: List of incident dictionaries
            
        Returns:
            DataFrame containing incident data
            
        Raises:
            ValueError: If json_data is empty or invalid
        """
        try:
            if not json_data:
                raise ValueError("Empty JSON data provided")
                
            df = pd.DataFrame(json_data)
            
            # Validate required columns
            required_columns = [
                'ID', 'Title', 'Description', 'Status', 'Priority',
                'Department', 'Category', 'Created_Date', 'Resolution_Date',
                'SLA_Status'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
            
            # Convert date columns to datetime
            date_columns = ['Created_Date', 'Resolution_Date']
            for col in date_columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            
            return df
            
        except Exception as e:
            logger.error(f"Error converting JSON to DataFrame: {str(e)}")
            raise
    
    def generate_report(
        self,
        incidents: List[Dict],
        output_format: str = "pdf",
        title: Optional[str] = None,
        css_file: Optional[Path] = None
    ) -> Path:
        """Generate an incident report.
        
        Args:
            incidents: List of incident dictionaries
            output_format: Output format (pdf or markdown)
            title: Optional report title
            css_file: Optional CSS file for styling
            
        Returns:
            Path to the generated report
            
        Raises:
            ValueError: If incidents list is empty or invalid
            RuntimeError: If report generation fails
        """
        try:
            # Convert to DataFrame
            df = self.json_to_dataframe(incidents)
            
            # Generate report title and filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_title = title or f"Incident Report - {timestamp}"
            filename = f"incident_report_{timestamp}"
            
            # Calculate metrics
            metrics = calculate_metrics(df)
            dept_analysis = analyze_departments(df)
            cat_analysis = analyze_categories(df)
            
            # Generate AI summary
            try:
                ai_summary = generate_summary(incidents)
                logger.info("Successfully generated AI summary")
            except Exception as e:
                logger.error(f"Failed to generate AI summary: {str(e)}")
                ai_summary = "AI summary generation failed. Please check the logs for details."
            
            # Create markdown content
            markdown_content = f"""# {report_title}

## Executive Summary
{ai_summary}

## Metrics Overview
- Total Incidents: {metrics['total_incidents']}
- Resolved Incidents: {metrics['resolved_incidents']}
- Resolution Rate: {metrics['resolution_rate']:.1f}%
- Average Resolution Time: {metrics['avg_resolution_time']:.1f} hours
- SLA Compliance Rate: {metrics['sla_compliance_rate']:.1f}%

## Department Analysis
{dept_analysis}

## Category Analysis
{cat_analysis}

## Priority Distribution
{df['Priority'].value_counts().to_markdown()}

## Status Distribution
{df['Status'].value_counts().to_markdown()}

## Recent Incidents
{df.sort_values('Created_Date', ascending=False).head().to_markdown()}

---
Report generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
            
            # Save markdown file
            markdown_path = self.output_dir / f"{filename}.md"
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Convert to PDF if requested
            if output_format.lower() == 'pdf':
                output_path = self.output_dir / f"{filename}.pdf"
                try:
                    markdown_to_pdf(
                        input_file=markdown_path,
                        output_file=output_path,
                        css_file=css_file,
                        title=report_title
                    )
                    logger.info(f"Successfully generated PDF report: {output_path}")
                    
                    # Clean up temporary markdown file
                    markdown_path.unlink()
                    
                    return output_path
                except Exception as e:
                    logger.error(f"Failed to convert to PDF: {str(e)}")
                    logger.info("Falling back to markdown format")
                    return markdown_path
            
            return markdown_path
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise RuntimeError(f"Failed to generate report: {str(e)}")
