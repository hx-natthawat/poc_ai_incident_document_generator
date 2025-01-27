"""Test script for the Incident Report Generator API - Development Environment."""
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
    base_url = "http://localhost:8080"  # Development port
    headers = {
        "X-API-Key": "b}1plG2b{dC8kjE"
    }
    
    print("Testing Incident Report Generator API (Development)...")
    
    # Test 1: Get sample data
    print("\n1. Testing GET /sample-data")
    try:
        response = requests.get(f"{base_url}/sample-data", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            incidents = data.get("incidents", [])
            print("✅ Successfully retrieved sample data")
            print(f"   Found {len(incidents)} incidents in sample data")
        else:
            print(f"❌ Failed to retrieve sample data: {response.status_code}")
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error accessing /sample-data: {e}")
    
    # Test 2: Generate report
    print("\n2. Testing POST /generate-report")
    try:
        # Get sample data first
        response = requests.get(f"{base_url}/sample-data", headers=headers)
        if response.status_code != 200:
            print(f"❌ Failed to get sample data: {response.status_code}")
            return
        
        # Generate report using sample data
        response = requests.post(
            f"{base_url}/generate-report",
            headers=headers,
            json=response.json()
        )
        
        if response.status_code == 200:
            print("✅ Successfully generated report")
            print(f"   Report saved as: {response.headers.get('X-Report-Filename', 'Unknown')}")
        else:
            print(f"❌ Failed to generate report: {response.status_code}")
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
    
    # Test 3: List reports
    print("\n3. Testing GET /reports/list")
    try:
        response = requests.get(
            f"{base_url}/reports/list",
            headers=headers,
            params={"limit": 5, "skip": 0}
        )
        
        if response.status_code == 200:
            data = response.json()
            reports = data.get("reports", [])
            print("✅ Successfully retrieved reports list")
            print(f"   Found {len(reports)} reports")
            for report in reports:
                print(f"   - {report['filename']} ({report['created_at']})")
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
            print("✅ Successfully retrieved latest report")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            print(f"   Content-Length: {response.headers.get('Content-Length')} bytes")
        else:
            print(f"❌ Failed to get latest report: {response.status_code}")
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error getting latest report: {e}")

if __name__ == "__main__":
    test_api()
