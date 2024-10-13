import requests
import json

# url = "http://127.0.0.1:8000/api/members/"
url = "https://wauu.uz/api/members/"

with open("members.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for member in data:
    response = requests.post(url, json=member)
    
    if response.status_code == 201:
        print(f"Member {member['name']} successfully added.")
    else:
        print(f"Failed to add {member['name']}. Status: {response.status_code}")
        print(f"Error: {response.text}")
