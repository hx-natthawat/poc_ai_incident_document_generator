"""PDF conversion utilities for incident reports."""
import os
import subprocess
from pathlib import Path
import logging
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)

def get_wkhtmltopdf_path() -> str:
    """Get the path to wkhtmltopdf executable.
    
    Returns:
        Path to wkhtmltopdf executable
        
    Raises:
        RuntimeError: If wkhtmltopdf is not found
    """
    # Check environment variable first
    wkhtmltopdf_path = os.getenv("WKHTMLTOPDF_PATH")
    if wkhtmltopdf_path and os.path.exists(wkhtmltopdf_path):
        return wkhtmltopdf_path
    
    # Try common installation paths
    common_paths = [
        "/usr/local/bin/wkhtmltopdf",  # Homebrew installation
        "/usr/bin/wkhtmltopdf",        # Linux installation
        "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"  # Windows installation
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    # Check if it's in PATH
    try:
        subprocess.run(["wkhtmltopdf", "--version"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
        return "wkhtmltopdf"
    except FileNotFoundError:
        raise RuntimeError(
            "wkhtmltopdf not found. Please install it and set WKHTMLTOPDF_PATH "
            "environment variable or add it to your system PATH."
        )

def markdown_to_pdf(
    input_file: Path,
    output_file: Path,
    css_file: Optional[Path] = None,
    title: Optional[str] = None
) -> None:
    """Convert markdown file to PDF using wkhtmltopdf.
    
    Args:
        input_file: Path to input markdown file
        output_file: Path to output PDF file
        css_file: Optional path to CSS file for styling
        title: Optional title for the PDF document
        
    Raises:
        FileNotFoundError: If input file or CSS file not found
        RuntimeError: If conversion fails
    """
    try:
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        if css_file and not css_file.exists():
            raise FileNotFoundError(f"CSS file not found: {css_file}")
        
        # Create output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Get wkhtmltopdf path
        wkhtmltopdf = get_wkhtmltopdf_path()
        
        # Convert markdown to HTML
        try:
            import markdown2
            with open(input_file, 'r', encoding='utf-8') as f:
                html_content = markdown2.markdown(
                    f.read(),
                    extras=['tables', 'fenced-code-blocks']
                )
        except ImportError:
            logger.warning("markdown2 not found, falling back to basic markdown")
            import markdown
            with open(input_file, 'r', encoding='utf-8') as f:
                html_content = markdown.markdown(
                    f.read(),
                    extensions=['tables', 'fenced_code']
                )
        
        # Create a temporary HTML file
        temp_html = input_file.with_suffix('.html')
        
        # Add CSS if provided
        css_content = ""
        if css_file:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
        
        # Create complete HTML document
        html_document = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title or 'Incident Report'}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f5f5f5;
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        {css_content}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""
        
        # Save temporary HTML file
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_document)
        
        # Convert to PDF
        options = [
            '--quiet',
            '--enable-local-file-access',
            '--margin-top', '20',
            '--margin-right', '20',
            '--margin-bottom', '20',
            '--margin-left', '20',
        ]
        
        try:
            subprocess.run(
                [wkhtmltopdf] + options + [str(temp_html), str(output_file)],
                check=True,
                capture_output=True,
                text=True
            )
            logger.info(f"Successfully converted {input_file} to PDF: {output_file}")
        finally:
            # Clean up temporary HTML file
            temp_html.unlink()
        
    except Exception as e:
        logger.error(f"Error converting markdown to PDF: {str(e)}")
        raise

def validate_wkhtmltopdf() -> bool:
    """Validate wkhtmltopdf installation.
    
    Returns:
        True if wkhtmltopdf is properly installed, False otherwise
    """
    try:
        wkhtmltopdf = get_wkhtmltopdf_path()
        result = subprocess.run(
            [wkhtmltopdf, '--version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error validating wkhtmltopdf: {str(e)}")
        return False
