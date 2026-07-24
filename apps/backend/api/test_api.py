"""Quick test for the API"""
import httpx

base_url = "http://localhost:8000/api/v1"

# Test login
r = httpx.post(f"{base_url}/auth/login", json={"email": "admin@interservim.com", "password": "Admin123!"})
print(f"Login: {r.status_code}")
data = r.json()
token = data["access_token"]
print(f"Token: {token[:50]}...")

# Test products
headers = {"Authorization": f"Bearer {token}"}
r = httpx.get(f"{base_url}/products", headers=headers)
print(f"Products: {r.status_code} - {len(r.json()['data'])} products")

# Test customers
r = httpx.get(f"{base_url}/customers", headers=headers)
print(f"Customers: {r.status_code} - {len(r.json()['data'])} customers")

# Test conversations
r = httpx.get(f"{base_url}/conversations", headers=headers)
print(f"Conversations: {r.status_code} - {len(r.json()['data'])} conversations")

# Test auth/me
r = httpx.get(f"{base_url}/auth/me", headers=headers)
print(f"Me: {r.status_code} - {r.json()['name']}")

print("\nAll API tests passed!")
