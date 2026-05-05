import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    store = os.getenv("SHOPIFY_STORE")
    client_id = os.getenv("SHOPIFY_CLIENT_ID")
    client_secret = os.getenv("SHOPIFY_CLIENT_SECRET")

    url = f"https://{store}/admin/oauth/access_token"

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    return response.json()["access_token"]

if __name__ == "__main__":
    token = get_access_token()
    print(f"Token acquired: {token[:10]}...")