import anthropic
import os
from dotenv import load_dotenv
from utils import strip_html
from enrichment import enrich_product_data
from products import get_products

load_dotenv()

def get_claude_results(enriched_product_data):
    client = anthropic.Anthropic()
    snippets = [r['snippet'] for r in enriched_product_data['serper_results']]
    system_prompt = "You are an expert e-commerce copywriter who specializes in Halloween and haunted house products."
    user_prompt = f"title: {enriched_product_data['product_detail']['title']}; body: {strip_html(enriched_product_data['product_detail']['body_html'])}; tags: {enriched_product_data['product_detail']['tags']}; price: {enriched_product_data['product_detail']['variants'][0]['price']}; Serper snippets: {snippets}"

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text

if __name__ == "__main__":
    test_id = get_products()[0]['id']
    enriched_test = enrich_product_data(test_id)
    print(get_claude_results(enriched_test))