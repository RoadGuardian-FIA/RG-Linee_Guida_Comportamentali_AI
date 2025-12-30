#!/usr/bin/env python3
"""
Simple test script to demonstrate the AI Behavioral Guidelines system
"""

import requests
import json
import time
import subprocess
import os
import sys

API_URL = "http://localhost:8000"


def wait_for_api(timeout=30):
    """Wait for the API to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{API_URL}/health")
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    return False


def test_endpoint(name, method, endpoint, data=None):
    """Test a single endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    url = f"{API_URL}{endpoint}"
    
    if method == "GET":
        response = requests.get(url)
    elif method == "POST":
        response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    
    try:
        json_data = response.json()
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Could not parse JSON response: {e}")
        print(response.text)
    
    return response.status_code == 200


def main():
    """Run all tests"""
    print("AI Behavioral Guidelines - Test Suite")
    print("="*60)
    
    # Check if API is running
    print("\nChecking if API is running...")
    if not wait_for_api(timeout=5):
        print("API is not running. Please start it with:")
        print("  python src/main.py")
        print("or:")
        print("  uvicorn src.main:app --reload")
        return 1
    
    print("✓ API is running")
    
    # Test root endpoint
    test_endpoint("Root Endpoint", "GET", "/")
    
    # Test health endpoint
    test_endpoint("Health Check", "GET", "/health")
    
    # Test protocols endpoint
    test_endpoint("Get All Protocols", "GET", "/protocols")
    
    # Test predict endpoint with various scenarios
    test_cases = [
        {
            "name": "Tamponamento ad alta gravità",
            "data": {
                "gravita": "high",
                "data_ora": "2024-01-15 08:30:00",
                "latitudine": 45.4642,
                "longitudine": 9.1900,
                "descrizione": "Tamponamento multiplo su autostrada",
                "categoria": "tamponamento"
            }
        },
        {
            "name": "Collisione con ostacolo a bassa gravità",
            "data": {
                "gravita": "low",
                "data_ora": "2024-01-15 14:20:00",
                "latitudine": 45.4700,
                "longitudine": 9.1850,
                "descrizione": "Veicolo contro guard-rail",
                "categoria": "collisione_con_ostacolo"
            }
        },
        {
            "name": "Investimento ad alta gravità",
            "data": {
                "gravita": "high",
                "data_ora": "2024-01-17 22:15:00",
                "latitudine": 45.4720,
                "longitudine": 9.1910,
                "descrizione": "Investimento pedone su strada urbana",
                "categoria": "investimento"
            }
        },
        {
            "name": "Incendio veicolo ad alta gravità",
            "data": {
                "gravita": "high",
                "data_ora": "2024-01-19 21:30:00",
                "latitudine": 45.4710,
                "longitudine": 9.1920,
                "descrizione": "Incendio veicolo in area urbana",
                "categoria": "incendio_veicolo"
            }
        }
    ]
    
    for test_case in test_cases:
        test_endpoint(
            f"Predict Protocol: {test_case['name']}", 
            "POST", 
            "/predict", 
            test_case['data']
        )
    
    # Test error handling
    test_endpoint(
        "Error Handling: Invalid Category",
        "POST",
        "/predict",
        {
            "gravita": "high",
            "data_ora": "2024-01-15 08:30:00",
            "latitudine": 45.4642,
            "longitudine": 9.1900,
            "descrizione": "Incidente non valido",
            "categoria": "invalid_category"
        }
    )
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
