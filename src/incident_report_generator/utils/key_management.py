"""API key management utilities."""
import os
import json
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class KeyManager:
    """Manages API key rotation and validation."""
    
    def __init__(self, keys_file: str = "api_keys.json"):
        """Initialize key manager."""
        self.keys_file = Path(keys_file)
        self.keys: Dict[str, dict] = {}
        self.load_keys()
    
    def load_keys(self):
        """Load API keys from file."""
        try:
            if self.keys_file.exists():
                with open(self.keys_file, 'r') as f:
                    self.keys = json.load(f)
        except Exception as e:
            logger.error(f"Error loading API keys: {e}")
            self.keys = {}
    
    def save_keys(self):
        """Save API keys to file."""
        try:
            with open(self.keys_file, 'w') as f:
                json.dump(self.keys, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving API keys: {e}")
    
    def generate_key(self, name: str, expires_in_days: int = 30) -> str:
        """Generate a new API key."""
        key = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        self.keys[key] = {
            "name": name,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expires_at.isoformat(),
            "is_active": True
        }
        
        self.save_keys()
        return key
    
    def validate_key(self, key: str) -> bool:
        """Validate an API key."""
        if key not in self.keys:
            return False
            
        key_info = self.keys[key]
        if not key_info["is_active"]:
            return False
            
        expires_at = datetime.fromisoformat(key_info["expires_at"])
        if datetime.utcnow() > expires_at:
            key_info["is_active"] = False
            self.save_keys()
            return False
            
        return True
    
    def revoke_key(self, key: str):
        """Revoke an API key."""
        if key in self.keys:
            self.keys[key]["is_active"] = False
            self.save_keys()
    
    def list_keys(self) -> Dict[str, dict]:
        """List all API keys."""
        return self.keys
    
    def cleanup_expired_keys(self):
        """Remove expired and inactive keys."""
        current_time = datetime.utcnow()
        active_keys = {}
        
        for key, info in self.keys.items():
            expires_at = datetime.fromisoformat(info["expires_at"])
            if info["is_active"] and current_time <= expires_at:
                active_keys[key] = info
        
        self.keys = active_keys
        self.save_keys()

# Example usage:
if __name__ == "__main__":
    # Initialize key manager
    key_manager = KeyManager()
    
    # Generate a new key
    new_key = key_manager.generate_key("test-key", expires_in_days=7)
    print(f"Generated key: {new_key}")
    
    # Validate the key
    is_valid = key_manager.validate_key(new_key)
    print(f"Key is valid: {is_valid}")
    
    # List all keys
    all_keys = key_manager.list_keys()
    print("All keys:", json.dumps(all_keys, indent=2))
    
    # Cleanup expired keys
    key_manager.cleanup_expired_keys()
