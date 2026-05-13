from claude import get_claude_results
from enrichment import enrich_product_data
from models import Product, EnrichedProduct

def full_product_pipeline(product_id):
        enriched = enrich_product_data(product_id)
        full_product = Product(enriched['product_detail'])
        full_enriched_product = EnrichedProduct(full_product, get_claude_results(enriched))
        return full_enriched_product

if __name__ == "__main__":
    from products import get_products
    products = get_products()
    full_product = full_product_pipeline(products[0]['id'])
    print(f"{full_product}")
