"""Main report generation module."""
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

from .utils.data_processing import (
    load_incident_data,
    calculate_sla_compliance,
    get_priority_breakdown,
    get_department_breakdown,
    get_category_breakdown
)
from .utils.ai_integration import AISummarizer
from .utils.pdf_converter import markdown_to_pdf

class IncidentReportGenerator:
    def __init__(self, data: Optional[pd.DataFrame] = None, data_file: Optional[Path] = None, template_file: Optional[Path] = None):
        self.base_dir = Path(__file__).parent.parent.parent
        self.data_file = data_file or (self.base_dir / "data" / "incident_data.csv")
        self.template_file = template_file or (self.base_dir / "templates" / "report_template.md")
        self.reports_dir = self.base_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        self.ai_summarizer = AISummarizer()
        self.data = data
        
    def generate_report(self) -> Tuple[str, Path, Path]:
        """Generate the complete incident report in both Markdown and PDF formats.
        
        Returns:
            Tuple containing:
            - Report content as string
            - Path to generated markdown file
            - Path to generated PDF file
        """
        # Load and process data
        if self.data is None:
            self.data = load_incident_data(self.data_file)
        
        # Calculate metrics
        metrics = self._calculate_metrics(self.data)
        
        # Generate Thai summary
        thai_summary = self.ai_summarizer.generate_thai_summary(metrics)
        
        # Render report
        report = self._render_report(metrics, thai_summary)
        
        # Save reports
        md_file, pdf_file = self._save_report(report)
        
        return report, md_file, pdf_file
    
    def json_to_dataframe(self, data: dict) -> pd.DataFrame:
        """Convert JSON data to pandas DataFrame."""
        df = pd.DataFrame(data["incidents"])
        # Convert datetime strings to pandas datetime
        df["Created_On"] = pd.to_datetime(df["Created_On"])
        df["Resolved_On"] = pd.to_datetime(df["Resolved_On"])
        return df
    
    def _calculate_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate all metrics for the report."""
        total, within_sla, breached_sla, compliance_rate = calculate_sla_compliance(df)
        resolved = len(df[df['Status'] == 'Resolved'])
        
        # Calculate resolution time for resolved incidents
        resolved_df = df[df["Status"] == "Resolved"].copy()
        resolved_df["resolution_time"] = (resolved_df["Resolved_On"] - resolved_df["Created_On"]).dt.total_seconds() / 3600
        avg_resolution_time = resolved_df["resolution_time"].mean() if not resolved_df.empty else 0
        
        # Priority breakdown
        priority_df = df.groupby("Priority").agg({
            "Incident_ID": "count",
            "Status": lambda x: sum(x == "Resolved"),
            "SLA_Status": lambda x: sum(x == "Within SLA")
        }).reset_index()
        
        priority_rows = []
        for _, row in priority_df.iterrows():
            total = row["Incident_ID"]
            resolved = row["Status"]
            unresolved = total - resolved
            sla_breaches = total - row["SLA_Status"]
            compliance_rate = (row["SLA_Status"] / total) * 100
            
            # Calculate average resolution time for this priority
            priority_resolved = resolved_df[resolved_df["Priority"] == row["Priority"]]
            avg_time = priority_resolved["resolution_time"].mean() if not priority_resolved.empty else 0
            
            priority_rows.append(
                f"{row['Priority']} | {total} | {resolved} | {unresolved} | "
                f"{sla_breaches} | {compliance_rate:.1f}% | {avg_time:.1f}"
            )
        
        # Department breakdown
        dept_df = df.groupby("Department").agg({
            "Incident_ID": "count",
            "Status": lambda x: sum(x == "Resolved"),
            "SLA_Status": lambda x: sum(x == "Within SLA")
        }).reset_index()
        
        dept_rows = []
        for _, row in dept_df.iterrows():
            total = row["Incident_ID"]
            resolved = row["Status"]
            unresolved = total - resolved
            sla_breaches = total - row["SLA_Status"]
            compliance_rate = (row["SLA_Status"] / total) * 100
            
            dept_rows.append(
                f"{row['Department']} | {total} | {resolved} | {unresolved} | "
                f"{sla_breaches} | {compliance_rate:.1f}%"
            )
        
        # Category breakdown
        cat_df = df.groupby("Category").agg({
            "Incident_ID": "count",
            "Status": lambda x: sum(x == "Resolved"),
            "SLA_Status": lambda x: sum(x == "Within SLA")
        }).reset_index()
        
        cat_rows = []
        for _, row in cat_df.iterrows():
            total = row["Incident_ID"]
            resolved = row["Status"]
            unresolved = total - resolved
            sla_breaches = total - row["SLA_Status"]
            compliance_rate = (row["SLA_Status"] / total) * 100
            
            cat_rows.append(
                f"{row['Category']} | {total} | {resolved} | {unresolved} | "
                f"{sla_breaches} | {compliance_rate:.1f}%"
            )
        
        # SLA summary
        sla_df = df.groupby("Priority").agg({
            "Incident_ID": "count",
            "SLA_Status": lambda x: sum(x == "Within SLA")
        }).reset_index()
        
        sla_rows = []
        for _, row in sla_df.iterrows():
            total = row["Incident_ID"]
            within_sla = row["SLA_Status"]
            breached = total - within_sla
            compliance_rate = (within_sla / total) * 100
            
            sla_rows.append(
                f"{row['Priority']} | {total} | {within_sla} | {breached} | "
                f"{compliance_rate:.1f}%"
            )
        
        # Incident list
        incident_rows = []
        for _, row in df.iterrows():
            resolved_on = row["Resolved_On"].strftime("%Y-%m-%d %H:%M") if pd.notna(row["Resolved_On"]) else "N/A"
            created_on = row["Created_On"].strftime("%Y-%m-%d %H:%M")
            
            incident_rows.append(
                f"{row['Incident_ID']} | {row['Title']} | {row['Priority']} | "
                f"{row['Department']} | {row['Status']} | {created_on} | "
                f"{resolved_on} | {row['SLA_Status']}"
            )
        
        return {
            'total_incidents': total,
            'resolved': resolved,
            'unresolved': total - resolved,
            'avg_resolution_time': f"{avg_resolution_time:.1f}",
            'sla_compliance_rate': f"{compliance_rate:.1f}",
            'priority_breakdown': "\n".join(priority_rows),
            'department_breakdown': "\n".join(dept_rows),
            'category_breakdown': "\n".join(cat_rows),
            'sla_summary': "\n".join(sla_rows),
            'incident_list': "\n".join(incident_rows),
            'report_period': {
                'start': df['Created_On'].min().strftime('%Y-%m-%d'),
                'end': df['Created_On'].max().strftime('%Y-%m-%d')
            }
        }
    
    def _render_report(self, metrics: Dict, thai_summary: str) -> str:
        """Render the report using the template."""
        with open(self.template_file, 'r') as f:
            template = f.read()
        
        report = template.format(
            start_date=metrics['report_period']['start'],
            end_date=metrics['report_period']['end'],
            generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_incidents=metrics['total_incidents'],
            resolved_incidents=metrics['resolved'],
            unresolved_incidents=metrics['unresolved'],
            avg_resolution_time=metrics['avg_resolution_time'],
            sla_compliance_rate=metrics['sla_compliance_rate'],
            thai_summary=thai_summary,
            priority_breakdown=metrics['priority_breakdown'],
            department_breakdown=metrics['department_breakdown'],
            category_breakdown=metrics['category_breakdown'],
            sla_summary=metrics['sla_summary'],
            incident_list=metrics['incident_list']
        )
        
        return report
    
    def _save_report(self, report: str) -> Tuple[Path, Path]:
        """Save the generated report in both Markdown and PDF formats.
        
        Returns:
            Tuple containing paths to the markdown and PDF files.
        """
        # Create reports directory if it doesn't exist
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filenames with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        md_file = self.reports_dir / f"incident_report_{timestamp}.md"
        pdf_file = self.reports_dir / f"incident_report_{timestamp}.pdf"
        
        # Save markdown
        with open(md_file, 'w') as f:
            f.write(report)
        
        # Convert to PDF
        markdown_to_pdf(md_file, pdf_file)
        
        return md_file, pdf_file
