import requests
import os
from dotenv import load_dotenv
from auth import get_access_token
from products import get_products

load_dotenv()

def get_product_detail(product_id):
    access_token = get_access_token()
    store = os.getenv("SHOPIFY_STORE")
    url = f"https://{store}/admin/api/2026-04/products/{product_id}.json"

    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["product"]

if __name__ == "__main__":
    products = get_products()
    prod_detail = get_product_detail(products[0]['id'])
    print(f"Title: {prod_detail['title']}")
    print(f"ID: {prod_detail['id']}")
    print(f"Price: {prod_detail['variants'][0]['price']}")
    print(f"Vendor: {prod_detail['vendor']}")
    print(f"Type: {prod_detail['product_type']}")
    print(f"Status: {prod_detail['status']}")
