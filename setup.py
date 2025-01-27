"""Setup file for the incident report generator package."""
from setuptools import setup, find_packages

setup(
    name="incident_report_generator",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.0.0",
        "python-dotenv>=1.0.0",
        "openai>=1.0.0",
        "jinja2>=3.0.0",
        "pytest>=7.0.0",
        "python-dateutil>=2.8.2",
        "markdown>=3.4.0",
        "pdfkit>=1.0.0",
        "Pillow>=10.0.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "python-multipart>=0.0.6",
    ],
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered incident report generator",
    keywords="incident, report, generator, ai",
)
