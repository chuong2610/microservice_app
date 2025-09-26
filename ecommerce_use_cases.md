# Core Use Cases - Search

## UC-S1: Keyword Search (Lexical + Semantic Hybrid)

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** User finds relevant products via a query.
- **Actors:** User, Search Service.
- **Preconditions:** Catalog indexed; user session started.
- **Trigger:** User submits query (e.g., “running shoes”).

**Expected Output:**

- Ranked product results with facets (filters).
- Hybrid retrieval applied: lexical (BM25) + semantic (vector ANN) + LTR re-ranking.
- Query logged for analytics.
- Acceptance criteria met (p95 latency ≤ 500 ms, zero-results rate ≤ threshold).

**Example Output:**

```json
{
  "query": "running shoes",
  "results": [
    {"product_id": "SKU12345", "title": "Nike Air Zoom Pegasus 40", "price": 120.0},
    {"product_id": "SKU98765", "title": "Adidas Ultraboost Light", "price": 180.0}
  ],
  "facets": {
    "brand": ["Nike", "Adidas", "Asics"],
    "price_range": ["$50-$100", "$100-$200"],
    "size": ["7","8","9","10"]
  },
  "latency_ms": 320
}
```

---

## UC-S2: Faceted Filtering & Sorting

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Narrow results using dynamic filters.
- **Actors:** User, Search Service.
- **Trigger:** User applies filters or sort options.

**Expected Output:**

- Filtered result set recomputed with updated facets.
- Sorting applied (relevance, price, rating).
- Clear indication if no results.

**Example Output:**

```json
{
  "query": "running shoes",
  "applied_filters": {"brand": "Nike", "size": "9"},
  "sort": "price_low_to_high",
  "results": [
    {"product_id": "SKU22222", "title": "Nike Revolution 6", "price": 70.0}
  ],
  "facets": {
    "brand": ["Nike","Adidas"],
    "size": ["8","9","10"]
  }
}
```

---

## UC-S3: Autosuggest / Autocomplete

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Reduce typing and guide users to discoverable queries/products.
- **Actors:** User, Search Service.
- **Trigger:** User types into search box.

**Expected Output:**

- Suggestions from past queries, trending queries, and products.
- Spell-corrected variants included.
- Results returned within 100–200 ms.

**Example Output:**

```json
{
  "input": "run",
  "suggestions": ["running shoes","running shorts","running socks"],
  "trending": ["marathon shoes","trail running shoes"]
}
```

---

## UC-S4: Semantic/Image-Aware Search

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Allow natural language or image queries.
- **Actors:** User, Search Service.
- **Trigger:** User submits free-form query or uploads image.

**Expected Output:**

- Embeddings generated for query/image.
- Relevant products retrieved via vector index.
- Results re-ranked with business rules.

**Example Output:**

```json
{
  "query_type": "image",
  "results": [
    {"product_id": "SKU55555","title":"Adidas Running Tee","price":35.0}
  ]
}
```

---

## UC-S5: Category/Browse Navigation

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Navigate product taxonomy without a query.
- **Actors:** User, Search Service.
- **Trigger:** User clicks category hierarchy.

**Expected Output:**

- Curated/ranked listings for category.
- Facets displayed for refinement.
- Rankings stable and fresh.

**Example Output:**

```json
{
  "category": "Shoes > Running",
  "results": [
    {"product_id":"SKU10101","title":"Asics Gel-Kayano 30","price":160.0}
  ],
  "facets": {
    "brand":["Asics","Nike","Adidas"]
  }
}
```

---

# Core Use Cases - Recommendations

## UC-R1: Personalized Home Feed

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Show a tailored landing experience.
- **Actors:** User, Recommendation Service.
- **Preconditions:** Anonymous or logged-in; features online.
- **Trigger:** User visits home page.

**Expected Output:**

- Personalized feed combining trending, affinities, new-in-stock, price-sensitive picks.
- Ranked with context (device, time, geo) and user features.
- Cold-start fallback to trending + contextual signals.

**Example Output:**

```json
{
  "feed": [
    {"product_id":"SKU11111","title":"Trending Sneakers","price":90.0},
    {"product_id":"SKU22222","title":"New Arrival Hoodie","price":55.0}
  ]
}
```

---

## UC-R2: PDP “Similar Items” (Item-to-Item)

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Keep users browsing closely related items.
- **Actors:** User, Recommendation Service.
- **Trigger:** User views a PDP.

**Expected Output:**

- Similar items fetched using embeddings + co-visitation.
- Out-of-stock items filtered out.

**Example Output:**

```json
{
  "base_item":"SKU12345",
  "similar_items":[
    {"product_id":"SKU12346","title":"Nike Air Zoom Pegasus 39","price":110.0},
    {"product_id":"SKU67890","title":"Adidas Solarboost","price":150.0}
  ]
}
```

---

## UC-R3: PDP “Frequently Bought Together” (Bundling)

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Increase basket size.
- **Actors:** User, Recommendation Service.
- **Trigger:** User views a PDP.

**Expected Output:**

- Cross-sell accessory bundles mined from historical orders.
- Bundles respect compatibility constraints.

**Example Output:**

```json
{
  "base_item":"SKU99999",
  "bundle":[
    {"product_id":"SKU88888","title":"Running Socks","price":15.0},
    {"product_id":"SKU77777","title":"Water Bottle","price":10.0}
  ]
}
```

---

## UC-R4: Cart Cross-Sell / Up-Sell

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Boost AOV with final-moment suggestions.
- **Actors:** User, Recommendation Service.
- **Trigger:** User views cart.

**Expected Output:**

- Complementary or premium alternatives suggested based on items in cart.
- Price elasticity and promotions considered.

**Example Output:**

```json
{
  "cart_items":["SKU12345"],
  "suggestions":[
    {"product_id":"SKU45678","title":"Premium Nike Running Shoes","price":150.0}
  ]
}
```

---

## UC-R5: Recently Viewed / Continue Browsing

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Reduce friction in resuming sessions.
- **Actors:** User, Recommendation Service.
- **Trigger:** User returns or scrolls on site.

**Expected Output:**

- Session-aware recommendations of recently viewed items.
- No stale or deleted items shown.

**Example Output:**

```json
{
  "recently_viewed":[
    {"product_id":"SKU11111","title":"Blue Running Jacket","price":75.0}
  ]
}
```

---

## UC-R6: Cold-Start Products Boosting

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Provide exposure to new items.
- **Actors:** User, Recommendation Service.
- **Trigger:** User browsing categories or feed.

**Expected Output:**

- New items surfaced using content-based similarity and controlled exploration.
- Merchandiser boosts applied.

**Example Output:**

```json
{
  "boosted_new":[
    {"product_id":"SKU20202","title":"Brand New Trail Shoes","price":140.0}
  ]
}
```

---

# Supporting Commerce Use Cases

## UC-C1: Product Detail View (PDP)

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Present complete, trustworthy product info; enable confident decisions.
- **Actors:** User, PDP Service.
- **Trigger:** User opens a product detail page.

**Expected Output:**

- Variant resolved, price/stock/ETA fetched.
- Media, specs, trust badges, and recommendations rendered.
- Acceptance: Correct price/stock/ETA; p95 ≤ 400 ms.

**Example Output:**

```json
{
  "product_id":"SKU12345",
  "title":"Nike Air Zoom Pegasus 40",
  "price":120.0,
  "stock":"In Stock",
  "eta":"2 days",
  "media":["image1.jpg","image2.jpg"],
  "trust_badges":["Verified","Free Returns"],
  "recommendations":["SKU54321","SKU67890"]
}
```

---

## UC-C2: Add to Cart / Save for Later

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Add items reliably; refresh high-intent recommendations.
- **Actors:** User, Cart Service.
- **Trigger:** User clicks "Add to Cart" or "Save for Later".

**Expected Output:**

- Purchasability validated, price/promos re-quoted.
- Cart line and totals persisted.
- Cross-sell/upsell refreshed.
- Acceptance: Accurate totals; p95 ≤ 250 ms; recs ≤ 300 ms.

**Example Output:**

```json
{
  "cart_id":"CART1001",
  "items":[
    {"product_id":"SKU12345","quantity":1,"price":120.0}
  ],
  "total":120.0,
  "recommendations":[
    {"product_id":"SKU88888","title":"Running Socks","price":15.0}
  ]
}
```

---

## UC-C3: Checkout & Payment

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Fast, secure purchase with fraud control and inventory commitment.
- **Actors:** User, Checkout Service, Payment Gateway.
- **Trigger:** User initiates checkout.

**Expected Output:**

- Checkout session locked, address/ship/tax quoted.
- Fraud pre-auth & payment auth completed.
- Inventory reserved, order created, confirmation returned.
- Acceptance: No double-charge; p95 auth ≤ 2s; correct tax/ship.

**Example Output:**

```json
{
  "order_id":"ORD56789",
  "status":"Confirmed",
  "payment_status":"Authorized",
  "shipping_address":"123 Main St, NY",
  "total":130.0,
  "estimated_delivery":"2025-09-28"
}
```

---

## UC-C4: Order Tracking & Returns

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Transparent tracking; self-serve returns/exchanges; suggest alternatives.
- **Actors:** User, Order Service, Carrier API.
- **Trigger:** User checks order or initiates return.

**Expected Output:**

- Order timeline and carrier ETA displayed.
- RMA/label generated if eligible.
- Refund within SLA.
- Alternatives suggested if item unavailable.

**Example Output:**

```json
{
  "order_id":"ORD56789",
  "status":"Shipped",
  "carrier":"UPS",
  "eta":"2025-09-29",
  "return_eligible":true,
  "rma_label_url":"https://returns.example.com/label123.pdf",
  "alternative_recommendations":["SKU43210"]
}
```

---

## UC-C5: Reviews & Q&A

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Gather high-quality UGC; enrich search/ranking with structured signals.
- **Actors:** User, Review Service, Moderation Service.
- **Trigger:** User submits review or Q&A.

**Expected Output:**

- Review/Q&A submitted with media.
- Auto/moderation applied, published if valid.
- Facets (e.g., “runs small”) extracted and indexed.
- Acceptance: No policy violations; enrichment ≤ 24h.

**Example Output:**

```json
{
  "product_id":"SKU12345",
  "review_id":"REV1001",
  "rating":5,
  "text":"Great shoes, but runs small.",
  "status":"Published",
  "facets":["runs_small"]
}
```

---

## UC-C6: Wishlist & Alerts

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Save items; notify on back-in-stock/price-drop; aid exploration.
- **Actors:** User, Wishlist Service.
- **Trigger:** User adds item to wishlist or subscribes alerts.

**Expected Output:**

- Items managed in wishlist.
- Alerts triggered on stock/price change.
- Notifications sent within SLA.
- Acceptance: Wishlist ops p95 ≤ 150 ms; alert accuracy 100%.

**Example Output:**

```json
{
  "wishlist_id":"WL1001",
  "items":[
    {"product_id":"SKU22222","title":"Adidas Ultraboost","price":180.0}
  ],
  "alerts":[
    {"type":"Price Drop","status":"Subscribed"}
  ]
}
```

---

# Admin & Operations Use Cases

## UC-A1: Catalog Management

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Create/update products, variants, pricing, taxonomy; preview impact.
- **Actors:** Admin, Catalog Service.
- **Trigger:** Admin edits product details.

**Expected Output:**

- Edits validated and previewed.
- Published and indexed within SLA.
- Acceptance: Publish→index ≤ 10 min (price/stock ≤ 2 min).

**Example Output:**

```json
{
  "product_id":"SKU33333",
  "title":"New Hoodie",
  "price":60.0,
  "status":"Published",
  "index_status":"Indexed"
}
```

---

## UC-A2: Synonym & Boost Rules

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Shape search intent/results with overrides.
- **Actors:** Admin, Search Config Service.
- **Trigger:** Admin configures synonyms/boost rules.

**Expected Output:**

- Synonyms added, boosts applied, conflicts checked.
- Instant rollback supported.
- Acceptance: Propagation ≤ 5 min; rollback ≤ 2 min.

**Example Output:**

```json
{
  "rule_id":"RULE101",
  "type":"Synonym",
  "query":"sneakers",
  "synonyms":["running shoes","trainers"],
  "status":"Active"
}
```

---

## UC-A3: Experiments Management

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Run A/B/M tests with guardrails and rollback.
- **Actors:** Admin, Experiment Service.
- **Trigger:** Admin defines and launches test.

**Expected Output:**

- Split users correctly, monitor guardrails.
- Auto-rollback if metrics breached.
- Acceptance: Guardrail trigger ≤ 5 min.

**Example Output:**

```json
{
  "experiment_id":"EXP2001",
  "hypothesis":"New ranking improves CTR",
  "split":{"A":50,"B":50},
  "status":"Running",
  "guardrails":"Zero-results rate < 5%"
}
```

---

## UC-A4: Data Quality & Drift Monitoring

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Detect schema/quality issues, freshness gaps, feature/model drift.
- **Actors:** Monitoring Service, Admin.
- **Trigger:** Continuous ingestion & monitoring.

**Expected Output:**

- Issues detected via schema/drift tests.
- Alerts generated and triaged.
- Mitigation via revert/retrain.
- Acceptance: SLAs met, low false positives.

**Example Output:**

```json
{
  "alert_id":"ALERT123",
  "issue":"Feature drift detected (PSI>0.2)",
  "status":"Open",
  "recommended_action":"Retrain model"
}
```

---

## UC-A5: Legal/Compliance

**UC Intent (Kích hoạt/điều kiện):**

- **Goal:** Fulfill DSARs; enforce consent/retention; gate restricted content.
- **Actors:** Compliance Officer, Legal Service.
- **Trigger:** DSAR request or compliance enforcement event.

**Expected Output:**

- DSAR verified and processed.
- Consent propagated across systems.
- Restricted content blocked in prohibited regions/ages.
- Acceptance: DSAR ≤ statutory deadline; consent ≤ 5 min.

**Example Output:**

```json
{
  "dsar_id":"DSAR999",
  "action":"Delete",
  "user_id":"USER555",
  "status":"Completed",
  "completion_time":"2025-09-24T10:00:00Z"
}
```
