"""Pytest configuration and fixtures for FastAPI tests"""
import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def clean_activities():
    """Provide a fresh copy of activities for each test"""
    return deepcopy(activities)


@pytest.fixture
def client(clean_activities, monkeypatch):
    """Provide TestClient with isolated activity data"""
    # Replace the global activities dict with clean copy for this test
    monkeypatch.setattr("src.app.activities", clean_activities)
    return TestClient(app)
