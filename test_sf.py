# test_sf.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Testing Salesforce Connection...")
print("=" * 50)

instance_url = "https://orgfarm-222ac0a3c9-dev-ed.develop.my.salesforce.com"
client_id = os.getenv('SF_CONSUMER_KEY')
client_secret = os.getenv('SF_CONSUMER_SECRET')

token_url = f"{instance_url}/services/oauth2/token"
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

print("Requesting access token...")
response = requests.post(token_url, data=data)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']
    print("✅ Got access token!")
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    query_url = f"{instance_url}/services/data/v58.0/query?q=SELECT+Id,Name+FROM+Account+LIMIT+5"
    query_response = requests.get(query_url, headers=headers)
    
    if query_response.status_code == 200:
        data = query_response.json()
        print(f"✅ Successfully queried accounts")
        print(f"📊 Found {data['totalSize']} accounts")
    else:
        print(f"❌ Query failed: {query_response.status_code}")
else:
    print(f"❌ Token request failed: {response.status_code}")
    print(response.text)