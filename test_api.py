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

    # Test 3: List reports
    print("\n3. Testing GET /reports")
    try:
        response = requests.get(
            f"{base_url}/reports",
            headers=headers,
            params={"limit": 5, "skip": 0}
        )
        
        if response.status_code == 200:
            data = response.json()
            reports = data.get("reports", [])
            total = data.get("total", 0)
            print("✅ Successfully retrieved report list")
            print(f"   Found {total} total reports")
            print(f"   Showing {len(reports)} reports")
            
            if reports:
                latest = reports[0]
                print(f"   Latest report: {latest['filename']}")
                print(f"   Created at: {latest['created_at']}")
        else:
            print(f"❌ Failed to list reports: {response.status_code}")
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error listing reports: {e}")

    # Test 4: Get latest report
    print("\n4. Testing GET /reports/latest")
    try:
        response = requests.get(f"{base_url}/reports/latest", headers=headers)
        
        if response.status_code == 200:
            # Save the PDF file
            content_disposition = response.headers.get('content-disposition', '')
            filename = content_disposition.split('filename=')[-1].strip('"')
            output_file = Path(f"latest_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
            
            with open(output_file, "wb") as f:
                f.write(response.content)
                
            print("✅ Successfully retrieved latest report")
            print(f"   Original filename: {filename}")
            print(f"   Saved to: {output_file}")
        elif response.status_code == 404:
            print("ℹ️ No reports found")
        else:
            print(f"❌ Failed to get latest report: {response.status_code}")
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error getting latest report: {e}")

if __name__ == "__main__":
    test_api()
