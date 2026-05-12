from utils import strip_html
from products import get_products
from claude import get_claude_results
from enrichment import enrich_product_data
from product_detail import get_product_detail

class Product:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = strip_html(data['body_html'])
        self.price = data['variants'][0]['price']
        self.vendor = data['vendor']
        self.product_type = data['product_type']
        self.status = data['status']
        self.image_count = len(data['images'])
        self.variant_count = len(data['variants'])

    def __repr__(self):
        return f"Product({self.id}: {self.title})"

class EnrichedProduct:
    def __init__(self, product, claude_result):
        self.product = product
        self.description = claude_result['description']
        self.seo_title = claude_result['seo_title']
        self.category = claude_result['category']
        self.tags = claude_result['tags']
        self.completeness_score = claude_result['completeness_score']
        self.completeness_flags = claude_result['completeness_flags']

    def __repr__(self):
        return f"EnrichedProduct({self.product})"

if __name__ == "__main__":
    products = get_products()
    enriched = enrich_product_data(products[0]['id'])
    sample_product = Product(enriched['product_detail'])
    sample_enriched_product = EnrichedProduct(sample_product, get_claude_results(enriched))
    print(sample_enriched_product)
    print(sample_enriched_product.completeness_score)
    print(sample_enriched_product.seo_title)