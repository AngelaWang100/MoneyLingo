#!/usr/bin/env python3
"""
Test script to demonstrate authentication flow
"""
import requests
import json

# Test JWT token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXJfMTIzIiwiZW1haWwiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzU5NzQ3NDQ1LCJpYXQiOjE3NTk2NjEwNDV9.y1FVxiAyAChBKfxvOvHxgeRTWiMIuhxSyaT7JY1wj8Q"

base_url = "http://localhost:8000"
headers = {"Authorization": f"Bearer {token}"}

print("🔐 Testing Authentication Flow")
print("=" * 50)

# Test 1: Health check (no auth required)
print("\n1. Testing Health Check (No Auth Required)")
try:
    response = requests.get(f"{base_url}/health")
    print(f"✅ Status: {response.status_code}")
    print(f"✅ Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Merchants (no auth required)
print("\n2. Testing Merchants Endpoint (No Auth Required)")
try:
    response = requests.get(f"{base_url}/api/v1/merchants")
    data = response.json()
    print(f"✅ Status: {response.status_code}")
    print(f"✅ Found {len(data['data'])} merchants")
    print(f"✅ First merchant: {data['data'][0]['name']}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Protected endpoint without auth
print("\n3. Testing Protected Endpoint (No Auth)")
try:
    response = requests.get(f"{base_url}/api/v1/customers")
    print(f"✅ Status: {response.status_code}")
    print(f"✅ Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Protected endpoint with auth
print("\n4. Testing Protected Endpoint (With Auth)")
try:
    response = requests.get(f"{base_url}/api/v1/customers", headers=headers)
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {len(data['data'])} customers")
        print(f"✅ First customer: {data['data'][0]['first_name']} {data['data'][0]['last_name']}")
    else:
        print(f"✅ Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: AI Features with auth
print("\n5. Testing AI Features (With Auth)")
try:
    payload = {
        "transaction_id": "test123",
        "language": "en"
    }
    response = requests.post(f"{base_url}/api/v1/explain-transaction", 
                           json=payload, headers=headers)
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Explanation: {data['explanation']}")
    else:
        print(f"✅ Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🎉 Authentication Test Complete!")
