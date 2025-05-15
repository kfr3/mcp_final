import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import json

from src.mcp_server import app
from database.config import get_db
from tests.conftest import test_data

client = TestClient(app)

def test_input_validation():
    """Test input validation for various endpoints"""
    # Test recipe search with invalid input
    invalid_payloads = [
        # Invalid ingredient type
        {"ingredients": "not_a_list", "dietary_restrictions": ["vegetarian"]},
        # Invalid dietary restriction type
        {"ingredients": ["tomato"], "dietary_restrictions": "not_a_list"},
        # Missing required fields
        {"ingredients": ["tomato"]},
        # Invalid cooking time type
        {"ingredients": ["tomato"], "dietary_restrictions": [], "max_cooking_time": "30"},
        # Invalid difficulty level
        {"ingredients": ["tomato"], "dietary_restrictions": [], "difficulty_level": 123}
    ]

    for payload in invalid_payloads:
        response = client.post("/tools/find_recipes", json=payload)
        assert response.status_code == 422  # Validation error

    # Test substitution with invalid input
    invalid_substitution_payloads = [
        # Invalid ingredient type
        {"ingredient": 123, "dietary_restrictions": ["vegan"]},
        # Invalid dietary restrictions type
        {"ingredient": "cheese", "dietary_restrictions": "vegan"},
        # Missing required fields
        {"ingredient": "cheese"},
        # Empty ingredient name
        {"ingredient": "", "dietary_restrictions": ["vegan"]}
    ]

    for payload in invalid_substitution_payloads:
        response = client.post("/tools/suggest_substitutions", json=payload)
        assert response.status_code == 422  # Validation error

def test_sql_injection_prevention():
    """Test SQL injection prevention"""
    # Test SQL injection in ingredient search
    sql_injection_payloads = [
        "'; DROP TABLE recipes; --",
        "' OR '1'='1",
        "'; SELECT * FROM users; --",
        "' UNION SELECT * FROM recipes; --"
    ]

    for payload in sql_injection_payloads:
        response = client.get(f"/ingredients/{payload}")
        assert response.status_code in [404, 422]  # Should not execute SQL injection

    # Test SQL injection in recipe search
    for payload in sql_injection_payloads:
        response = client.post("/tools/find_recipes", json={
            "ingredients": [payload],
            "dietary_restrictions": ["vegetarian"]
        })
        assert response.status_code == 422  # Should not execute SQL injection

def test_error_message_security():
    """Test that error messages don't expose sensitive information"""
    # Test database error handling
    response = client.get("/recipe/999999")  # Non-existent recipe
    assert response.status_code == 404
    error_data = response.json()
    assert "error" in error_data
    assert "database" not in error_data["error"].lower()
    assert "sql" not in error_data["error"].lower()
    assert "stack trace" not in error_data["error"].lower()

    # Test validation error messages
    response = client.post("/tools/find_recipes", json={
        "ingredients": ["tomato"],
        "dietary_restrictions": 123  # Invalid type
    })
    assert response.status_code == 422
    error_data = response.json()
    assert "detail" in error_data
    assert "database" not in str(error_data).lower()
    assert "sql" not in str(error_data).lower()
    assert "stack trace" not in str(error_data).lower()

def test_rate_limiting():
    """Test rate limiting functionality"""
    # Make multiple requests in quick succession
    for _ in range(10):
        response = client.get("/ingredients/vegetables")
        assert response.status_code in [200, 429]  # 429 is Too Many Requests

    # Test rate limit headers
    response = client.get("/ingredients/vegetables")
    if response.status_code == 429:
        assert "Retry-After" in response.headers
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers

def test_cors_security():
    """Test CORS security headers"""
    response = client.get("/ingredients/vegetables")
    assert response.status_code == 200
    
    # Check security headers
    assert "Access-Control-Allow-Origin" in response.headers
    assert "Access-Control-Allow-Methods" in response.headers
    assert "Access-Control-Allow-Headers" in response.headers
    
    # Verify allowed origins
    allowed_origins = response.headers["Access-Control-Allow-Origin"]
    assert allowed_origins in ["*", "http://localhost:3000"]  # Adjust based on your CORS policy

def test_content_security():
    """Test content security headers"""
    response = client.get("/ingredients/vegetables")
    assert response.status_code == 200
    
    # Check security headers
    assert "Content-Security-Policy" in response.headers
    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers
    assert "X-XSS-Protection" in response.headers
    
    # Verify content type
    assert response.headers["Content-Type"] == "application/json" 