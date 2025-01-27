"""OpenAI integration for generating summaries."""
import os
from typing import Dict
from openai import OpenAI
from ..config import DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE, TECHNICAL_TERMS

class AISummarizer:
    """Class for generating AI-powered summaries."""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        """Initialize the AI summarizer."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
    
    def generate_thai_summary(self, metrics: Dict) -> str:
        """Generate a Thai summary of the incident report.
        
        Preserves specified technical terms in English while translating
        the rest to Thai.
        """
        # Create prompt with technical term preservation instructions
        terms_list = ", ".join(TECHNICAL_TERMS)
        prompt = f"""
        Please generate a Thai language executive summary of this incident report.
        Keep these technical terms in English: {terms_list}
        
        Report Metrics:
        - Total Incidents: {metrics['total_incidents']}
        - Resolved: {metrics['resolved']}
        - Unresolved: {metrics['unresolved']}
        - Average Resolution Time: {metrics['avg_resolution_time']} hours
        - SLA Compliance Rate: {metrics['sla_compliance_rate']}%
        
        The summary should:
        1. Be professional and concise
        2. Focus on key metrics and trends
        3. Highlight significant findings
        4. Keep specified technical terms in English
        5. Use proper Thai language structure
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional incident report analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return (
                "ไม่สามารถสร้างสรุปรายงานอัตโนมัติได้ในขณะนี้ "
                "กรุณาตรวจสอบการเชื่อมต่อกับ OpenAI API และลองใหม่อีกครั้ง"
            )
