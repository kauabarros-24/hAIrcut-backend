import requests
	
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyMTA3MC1kMmE1LTQ3OTUtODI4Zi1kNjRmMTlkYjJjMWYiLCJleHAiOjE3NjA0ODU4MjF9.FQnF6JUB75WGZ_MSfhztgubDIgQLZWXN36vzPiH01q8"
token_type = "bearer"
url = "http://localhost:8000/api/user/me"


headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(url=url, headers=headers)

if response.status_code == 200:
    user_data = response.json()
    print("Usuário autenticado:", user_data)
else:
    print(f"Erro {response.status_code}: {response.text}")


