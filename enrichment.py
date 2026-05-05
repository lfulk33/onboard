from utils import clean_query
from product_detail import get_product_detail
from products import get_products
from serper import get_serper_results

def enrich_product_data(product_id):
    product_detail = get_product_detail(product_id)
    cleaned_title = clean_query(product_detail['title'])
    serper_results = get_serper_results(cleaned_title)
    return {"product_detail":product_detail, "serper_results":serper_results}

if __name__ == "__main__":
    test_id = get_products()[0]['id']
    print(enrich_product_data(test_id))