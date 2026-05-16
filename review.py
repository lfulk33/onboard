def review_batch(enriched_products):
    approved = []
    rejected = []

    for ep in enriched_products:
        print(f"\n{'='*60}")
        print(f"PRODUCT: {ep.product.title}")
        print(f"COMPLETENESS SCORE: {ep.completeness_score}/10")
        print(f"FLAGS: {', '.join(ep.completeness_flags)}")
        print(f"\nSEO TITLE: {ep.seo_title}")
        print(f"CATEGORY: {ep.category}")
        print(f"TAGS: {', '.join(ep.tags)}")
        print(f"\nDESCRIPTION:\n{ep.description}")
        print(f"{'='*60}")

        decision = input("\nApprove this product? (y/n/q to quit): ").strip().lower()

        if decision == 'y':
            approved.append(ep)
            print("Approved.")
        elif decision == 'q':
            print("Quitting review.")
            break
        else:
            rejected.append(ep)
            print("Rejected.")

    print(f"\nReview complete. Approved: {len(approved)}, Rejected: {len(rejected)}")
    return approved, rejected


if __name__ == "__main__":
    from batch import run_batch
    results = run_batch(limit=3)
    approved, rejected = review_batch(results)