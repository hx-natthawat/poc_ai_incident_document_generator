"""Run the FastAPI server."""
import os
import uvicorn
from dotenv import load_dotenv

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8080"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    # Run server
    uvicorn.run(
        "incident_report_generator.api:app",
        host=host,
        port=port,
        reload=debug
    )
