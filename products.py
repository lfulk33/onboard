import requests
import os
from dotenv import load_dotenv
from auth import get_access_token

load_dotenv()

def get_products():
    access_token = get_access_token()
    store = os.getenv("SHOPIFY_STORE")
    url = f"https://{store}/admin/api/2026-04/products.json"

    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["products"]

if __name__ == "__main__":
    products = get_products()
    print(f"Total Products: {len(products)}")
    for product in products:
        print(f"{product['title']}")