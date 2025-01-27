"""Test script for the Incident Report Generator API."""
import json
import os
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

def test_api():
    """Test the API endpoints."""
    # Load environment variables
    load_dotenv()
    
    # API base URL and headers
    base_url = "http://localhost:8080"
    headers = {
        "X-API-Key": os.getenv("API_KEY", "your-api-key-here")
    }
    
    print("Testing Incident Report Generator API...")
    
    # Test 1: Get sample data
    print("\n1. Testing GET /sample-data")
    try:
        response = requests.get(f"{base_url}/sample-data", headers=headers)
        if response.status_code == 200:
            print("✅ Successfully retrieved sample data")
            sample_data = response.json()
            print(f"   Found {len(sample_data['incidents'])} incidents in sample data")
        else:
            print(f"❌ Failed to get sample data: {response.status_code}")
            if response.headers.get("content-type") == "application/json":
                print(f"   Error: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Error accessing /sample-data: {e}")
        return

    # Test 2: Generate report from sample data
    print("\n2. Testing POST /generate-report")
    try:
        # Generate report
        response = requests.post(
            f"{base_url}/generate-report",
            json=sample_data,
            headers=headers
        )
        
        if response.status_code == 200:
            # Create reports directory if it doesn't exist
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            # Save the PDF with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_file = reports_dir / f"incident_report_{timestamp}.pdf"
            
            with open(pdf_file, "wb") as f:
                f.write(response.content)
            print("✅ Successfully generated report")
            print(f"   Report saved as {pdf_file}")
        else:
            print(f"❌ Failed to generate report: {response.status_code}")
            if response.headers.get("content-type") == "application/json":
                print(f"   Error: {response.json()}")
            else:
                print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
    finally:
        # Cleanup test data file
        Path("test_data.json").unlink(missing_ok=True)

if __name__ == "__main__":
    test_api()
