"""Run the FastAPI application."""
import os
import uvicorn
from src.incident_report_generator.api import app

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))  # Changed from 8080 to 8000
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    # Configure logging
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    
    uvicorn.run(
        app=app,
        host=host,
        port=port,
        reload=debug,
        log_config=log_config
    )
