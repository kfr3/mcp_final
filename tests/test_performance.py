import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.mcp_server import app
from database.config import get_db
from tests.conftest import test_data

client = TestClient(app)

def measure_response_time(func):
    """Decorator to measure response time of a function"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, end_time - start_time
    return wrapper

@measure_response_time
def get_ingredients_by_category(category: str):
    """Get ingredients by category and measure response time"""
    return client.get(f"/ingredients/{category}")

@measure_response_time
def find_recipes(payload: dict):
    """Find recipes and measure response time"""
    return client.post("/tools/find_recipes", json=payload)

@measure_response_time
def suggest_substitutions(payload: dict):
    """Suggest substitutions and measure response time"""
    return client.post("/tools/suggest_substitutions", json=payload)

def test_database_query_performance(test_data):
    """Test database query performance"""
    # Test ingredient category query
    response, time_taken = get_ingredients_by_category("vegetables")
    assert response.status_code == 200
    assert time_taken < 0.1  # Should respond within 100ms

    # Test recipe search query
    payload = {
        "ingredients": ["tomato", "cheese"],
        "dietary_restrictions": ["vegetarian"]
    }
    response, time_taken = find_recipes(payload)
    assert response.status_code == 200
    assert time_taken < 0.2  # Should respond within 200ms

    # Test substitution query
    payload = {
        "ingredient": "cheese",
        "dietary_restrictions": ["vegan"]
    }
    response, time_taken = suggest_substitutions(payload)
    assert response.status_code == 200
    assert time_taken < 0.15  # Should respond within 150ms

def test_concurrent_requests(test_data):
    """Test handling of concurrent requests"""
    # Prepare test payloads
    find_recipes_payload = {
        "ingredients": ["tomato", "cheese"],
        "dietary_restrictions": ["vegetarian"]
    }
    substitution_payload = {
        "ingredient": "cheese",
        "dietary_restrictions": ["vegan"]
    }

    # Create a list of tasks
    tasks = [
        (find_recipes, find_recipes_payload),
        (suggest_substitutions, substitution_payload),
        (get_ingredients_by_category, "vegetables"),
        (get_ingredients_by_category, "dairy")
    ]

    # Execute tasks concurrently
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(task[0], task[1])
            for task in tasks
        ]
        results = [future.result() for future in futures]
    end_time = time.time()

    # Verify all requests were successful
    for response, _ in results:
        assert response.status_code == 200

    # Verify total execution time
    total_time = end_time - start_time
    assert total_time < 0.5  # All concurrent requests should complete within 500ms

def test_memory_usage(test_data):
    """Test memory usage during operations"""
    import psutil
    import os

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    # Perform a series of operations
    for _ in range(10):
        get_ingredients_by_category("vegetables")
        find_recipes({
            "ingredients": ["tomato", "cheese"],
            "dietary_restrictions": ["vegetarian"]
        })
        suggest_substitutions({
            "ingredient": "cheese",
            "dietary_restrictions": ["vegan"]
        })

    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory

    # Memory increase should be reasonable (less than 10MB)
    assert memory_increase < 10 * 1024 * 1024  # 10MB in bytes

def test_caching_effectiveness(test_data):
    """Test caching effectiveness for repeated requests"""
    # First request
    response1, time1 = get_ingredients_by_category("vegetables")
    assert response1.status_code == 200

    # Second request (should be faster due to caching)
    response2, time2 = get_ingredients_by_category("vegetables")
    assert response2.status_code == 200

    # Verify that the second request was faster
    assert time2 < time1

    # Verify that the responses are identical
    assert response1.json() == response2.json() 