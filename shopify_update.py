import requests
import os
import logging
from dotenv import load_dotenv
from auth import get_access_token

load_dotenv()

def update_product(enriched_product):
    try:
        store = os.getenv("SHOPIFY_STORE")
        token = get_access_token()

        url = f"https://{store}/admin/api/2026-04/products/{enriched_product.product.id}.json"

        headers = {
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json"
        }

        payload = {
            "product": {
                "id": enriched_product.product.id,
                "body_html": enriched_product.description,
                "product_type": enriched_product.category,
                "tags": ", ".join(enriched_product.tags)
            }
        }

        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["product"]
    except Exception as e:
        logging.error(f"Failed to update product {enriched_product.product.id}: {e}")
        raise

if __name__ == "__main__":
    from batch import run_batch
    from review import review_batch
    results = run_batch(limit=1)
    approved, rejected = review_batch(results)
    for ep in approved:
        updated = update_product(ep)
        print(f"Updated: {updated['title']}")