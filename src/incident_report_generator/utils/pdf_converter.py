"""PDF conversion utilities."""
import os
from pathlib import Path
import markdown
import pdfkit

def markdown_to_pdf(markdown_file: Path, output_file: Path) -> None:
    """Convert markdown file to PDF using pdfkit (wkhtmltopdf)."""
    try:
        # Read markdown content
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=['tables', 'attr_list', 'md_in_html']
        )
        
        # Add HTML wrapper with styling
        css = """
            @page {
                size: A4;
                margin: 2.5cm;
            }
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 100%;
                margin: 0;
                padding: 0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 10pt;
                page-break-inside: avoid;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
                word-wrap: break-word;
            }
            th {
                background-color: #f5f5f5;
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            h1 {
                color: #2c3e50;
                font-size: 24pt;
                text-align: center;
                margin-top: 0;
            }
            h2 {
                color: #2c3e50;
                font-size: 16pt;
                margin-top: 20px;
                page-break-before: always;
            }
            h2:first-of-type {
                page-break-before: avoid;
            }
            hr {
                border: none;
                border-top: 1px solid #ddd;
                margin: 20px 0;
            }
            ul {
                margin: 0;
                padding-left: 20px;
            }
            li {
                margin: 5px 0;
            }
            p {
                margin: 10px 0;
            }
        """
        
        html_doc = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Incident Report</title>
            <style>{css}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Get wkhtmltopdf path from environment
        wkhtmltopdf_path = os.getenv("WKHTMLTOPDF_PATH", "/usr/local/bin/wkhtmltopdf")
        
        # Configure PDF options
        options = {
            'page-size': 'A4',
            'margin-top': '25mm',
            'margin-right': '25mm',
            'margin-bottom': '25mm',
            'margin-left': '25mm',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
            'quiet': None
        }
        
        # Configure pdfkit
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        
        # Convert to PDF
        pdfkit.from_string(html_doc, str(output_file), options=options, configuration=config)
        
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        # Create a simple text version as fallback
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(output_file.with_suffix('.txt'), 'w', encoding='utf-8') as f:
            f.write(content)
        print("Created text file as fallback")
