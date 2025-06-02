"""
Configuration settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API Key
AVIATION_STACK_API_KEY = os.getenv("AVIATION_STACK_API_KEY")

# Default server settings
DEFAULT_PORT = 3001
DEFAULT_CONNECTION_TYPE = "stdio"  # Alternative: "stdio"
