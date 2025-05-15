import os
from dotenv import load_dotenv

load_dotenv()

# MCP Server Configuration
MCP_HOST = os.getenv("MCP_HOST", "localhost")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))
MCP_DEBUG = os.getenv("MCP_DEBUG", "False").lower() == "true"

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recipe_bot.db")

# Recipe Bot Configuration
MAX_RECIPES_PER_REQUEST = int(os.getenv("MAX_RECIPES_PER_REQUEST", "10"))
DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 