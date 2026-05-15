from products import get_products
from pipeline import full_product_pipeline
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_batch(delay=2, limit=None):
    all_products = get_products()
    if limit:
        all_products = all_products[:limit]
    results = []   
    for product in all_products:
        try:
            logging.info(f"Processing: {product['title']}")
            enriched_product = full_product_pipeline(product['id'])
            results.append(enriched_product)
            time.sleep(delay)
        except Exception as e:
            logging.error(f"Failed on {product['title']}: {e}")
            continue
    logging.info(f"Batch complete. {len(results)} of {len(all_products)} products processed.")
    return results

if __name__ == "__main__":
    results = run_batch(limit=3)
    print(f"Returned {len(results)} EnrichedProduct objects")