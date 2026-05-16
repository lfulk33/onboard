# ONBOARD

**AI-powered merchant catalog onboarding tool for Shopify**

ONBOARD connects to a Shopify store, enriches each product with live competitive search data, and uses Claude to generate production-ready descriptions, normalized categories, SEO-optimized titles, and completeness scores. A human approval step gates every change before anything writes back to the store.

---

## The Problem

New merchants onboard with messy product catalogs. Inconsistent categories, missing descriptions, SKU numbers as titles, no SEO consideration. Before anything can go live, someone has to clean it. At small merchants that person is the merchant. At mid-market it is usually the SE or TAM holding their hand. It is slow, manual, and does not scale.

## The Solution

A three-API pipeline that automates the cleanup with a human in the loop:

1. **Retrieve** — Shopify Admin API pulls the live product catalog
2. **Enrich** — Serper API searches each product and returns competitive context showing how the market describes similar items
3. **Reason** — Claude receives both the raw product data and the enrichment context, then returns structured JSON with improved descriptions, normalized categories, SEO titles, completeness scores, and flags
4. **Review** — Flask UI presents Claude's output side by side with the original for human approval
5. **Act** — Approved changes write back to Shopify via the Admin API

---

## Architecture

```
products.py          → Shopify: fetch product list
product_detail.py    → Shopify: fetch full product detail
serper.py            → Serper: pull competitive search context
enrichment.py        → Orchestrate Shopify + Serper into one enriched object
claude.py            → Anthropic: generate structured JSON output
models.py            → Product and EnrichedProduct classes
pipeline.py          → Single product end-to-end
batch.py             → Full catalog batch processing with rate limiting and error handling
shopify_update.py    → Shopify: write approved changes back
review.py            → Terminal-based approval interface
app.py               → Flask web approval UI
utils.py             → HTML stripping, query cleaning utilities
```

---

## Tech Stack

| Component | Tool |
|---|---|
| Language | Python 3 |
| E-commerce API | Shopify Admin API |
| Search Enrichment | Serper API |
| AI Reasoning | Anthropic API (Claude Sonnet 4.6) |
| Web Framework | Flask |
| Environment | python-dotenv |
| HTTP | requests |
| HTML Parsing | BeautifulSoup4 |

---

## Claude Output (Structured JSON)

Every product returns a structured JSON object with six fields:

```json
{
  "description": "Clean rewritten product description, no markdown",
  "seo_title": "SEO optimized title for search",
  "category": "Normalized product type",
  "tags": ["tag1", "tag2", "tag3"],
  "completeness_score": 7,
  "completeness_flags": ["no images", "outdated shipping notice"]
}
```

---

## Flask Review UI

The approval interface shows each product's original and proposed content side by side with completeness score, flags, SEO title, category, and tags visible before any decision is made. Approved products write directly to Shopify. Rejected products are skipped.

---

## Setup

### Prerequisites

- Python 3.10+
- Shopify Partner account with a development store
- Serper API key (serper.dev)
- Anthropic API key (console.anthropic.com)

### Installation

```bash
git clone https://github.com/lfulk33/onboard.git
cd onboard
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```
SHOPIFY_CLIENT_ID=your_client_id
SHOPIFY_CLIENT_SECRET=your_client_secret
SHOPIFY_STORE=your-store.myshopify.com
SERPER_API_KEY=your_serper_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### Run

```bash
# Full pipeline with Flask UI
python3 app.py

# Batch processing only (terminal)
python3 batch.py

# Single product test
python3 pipeline.py
```

---

## Key Design Decisions

**Retrieval-Augmented Generation.** Claude doesn't generate descriptions in a vacuum. Each product is enriched with live Serper search results before the prompt is built, giving Claude competitive market context. The output quality difference versus a naive prompt is significant.

**Human in the loop.** The approval step is a deliberate architectural choice. In a real merchant onboarding scenario you cannot have AI writing to a live store without a human reviewing the output. Every approved change is intentional, not automatic.

**Separation of concerns.** Each file has one job. Shopify auth, product retrieval, search enrichment, AI reasoning, batch orchestration, and write-back are all isolated. Debugging a failure in any one stage doesn't require understanding the others.

**Structured output.** Claude returns JSON, not prose. This makes the output programmatically useful rather than just readable, enabling discrete field updates to Shopify rather than a single blob replacement.

---

## What I Learned

This project taught me the core pattern behind enterprise AI integrations: retrieve structured data, enrich it with external context, pass both to an LLM with a precise prompt, parse structured output, and gate action on human review. That pattern applies to nearly any domain where AI needs to reason about real business data.

The agentic review loop was the most interesting architectural decision. Choosing where human oversight fits in an automated workflow is not a technical question, it is a product question. For a tool that writes to a live store, the answer is: before the write, every time.

---

## Author

Larry Fulkerson — Senior Solutions Engineer  
[GitHub](https://github.com/lfulk33) | [LinkedIn](https://linkedin.com/in/larryfulkerson)

---

## Project Context

Built as Portfolio Project 2 in a self-directed technical learning track focused on AI-native application development. Portfolio Project 1: [plaid-explorer](https://github.com/lfulk33/plaid-explorer) — a Python-based Plaid API integration covering auth, transactions, webhooks, and data export.
