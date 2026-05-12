import anthropic
import os
import json
from dotenv import load_dotenv
from utils import strip_html
from enrichment import enrich_product_data
from products import get_products

load_dotenv()

def get_claude_results(enriched_product_data):
    client = anthropic.Anthropic()
    snippets = [r['snippet'] for r in enriched_product_data['serper_results']]
    system_prompt = """You are an expert e-commerce copywriter who specializes in Halloween and 
    haunted house products. I need the following info returned only in JSON format, no other text at all.
    The field 'completeness_score' rate 1-10 based on quality of existing description, presence of images, tags, and variant data.
    The field 'completeness_flags' are used to flag specific issues like  "missing description", "no images", "thin tags", "no SEO title."
    Here's the full set we want back, example shown below: 
    {
        "description": "string - clean rewritten product description, no markdown",
        "seo_title":  "string - SEO optimized title",
        "category": "string - normalized product type", 
        "tags": ["string", "string"],
        "completeness_score": 8, 
        "completeness_flags": ["string", "string"]
    }
    Return only the JSON object. No explanation, no markdown, no code blocks.
    """
    user_prompt = f"title: {enriched_product_data['product_detail']['title']}; body: {strip_html(enriched_product_data['product_detail']['body_html'])}; tags: {enriched_product_data['product_detail']['tags']}; price: {enriched_product_data['product_detail']['variants'][0]['price']}; # variants: {len(enriched_product_data['product_detail']['variants'])}; # of images: {len(enriched_product_data['product_detail']['images'])}; Serper snippets: {snippets}"

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    return json.loads(response.content[0].text)

if __name__ == "__main__":
    test_id = get_products()[0]['id']
    enriched_test = enrich_product_data(test_id)
    result = get_claude_results(enriched_test)
    print(type(result))
    print(result['completeness_score'])