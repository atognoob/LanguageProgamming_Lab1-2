import requests

# Test GET /
print("Testing GET /")
response = requests.get('http://127.0.0.1:8000/')
print(response.text)

# Test GET /<tz_name>
print("\nTesting GET /<tz_name>")
for tz_name in ["Europe/London", "Asia/Ho_Chi_Minh", "America/New_York"]:
    response = requests.get(f'http://127.0.0.1:8000/{tz_name}')
    print(f"Time in {tz_name}: {response.text}")

# Test POST /api/v1/time
print("\nTesting POST /api/v1/time")
response = requests.post('http://127.0.0.1:8000/api/v1/time', json={"tz": "Asia/Tokyo"})
print(response.json())

# Test POST /api/v1/date
print("\nTesting POST /api/v1/date")
response = requests.post('http://127.0.0.1:8000/api/v1/date', json={"tz": "UTC"})
print(response.json())

# Test POST /api/v1/datediff
print("\nTesting POST /api/v1/datediff")
response = requests.post('http://127.0.0.1:8000/api/v1/datediff', json={
    "start": {"date": "1.1.2023 10:30:00", "tz": "Asia/Tokyo"},
    "end": {"date": "1.26.2023 9:34:00", "tz": "Europe/Paris"}
})
print(response.json())
