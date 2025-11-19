"""
Quick test script to verify R2R API access with secret key
"""

import requests
import json

API_BASE = "http://136.119.36.216:7272"
SECRET_KEY = "3276b4262bcfa6a267a7989b4feb0b169b806afa8494aa7d4ab2e435272c433a"

print("Testing R2R API with Secret Key...")
print("="*60)

# Test different authentication methods
auth_methods = [
    ("Bearer Token", {"Authorization": f"Bearer {SECRET_KEY}"}),
    ("X-API-Key", {"X-API-Key": SECRET_KEY}),
    ("R2R-Secret-Key", {"R2R-Secret-Key": SECRET_KEY}),
    ("No Auth", {}),
]

endpoints = [
    "/v3/health",
    "/health",
    "/",
    "/docs",
    "/openapi.json",
]

for endpoint in endpoints:
    print(f"\n--- Testing: {endpoint} ---")

    for method_name, headers in auth_methods:
        try:
            response = requests.get(
                f"{API_BASE}{endpoint}",
                headers=headers,
                timeout=5
            )

            print(f"  {method_name}: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"    Response: {json.dumps(data, indent=4)[:200]}")
                except:
                    print(f"    Response: {response.text[:200]}")
                break  # Found working method

        except requests.exceptions.RequestException as e:
            print(f"  {method_name}: ERROR - {str(e)[:50]}")

    print()

print("="*60)
print("Test completed")
