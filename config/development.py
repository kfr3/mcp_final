"""
Development configuration settings
"""

import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recipe_bot.db")

# API settings
API_V1_PREFIX = "/api/v1"
DEBUG = True
HOST = "0.0.0.0"
PORT = 8000

# CORS settings
CORS_ORIGINS = [
    "http://localhost:3000",  # Frontend development server
    "http://localhost:8000",  # API development server
]

# Logging settings
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Testing settings
TEST_DATABASE_URL = "sqlite:///./test_recipe_bot.db" 