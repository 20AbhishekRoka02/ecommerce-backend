# Backend and API reference

This document describes the API as currently implemented. It is intended for
the Next.js frontend and should be updated if routes, serializers, or response
behavior change.

## Project overview

- Django REST Framework backend; frontend is a separate application.
- Product catalog organized by category, with business details in
  `CompanyConfig`.
- Admin-managed data and read-only public API. Login, cart, checkout, orders,
  and payment APIs are not implemented.
- Media storage and Render persistent-disk setup are documented in
  [MEDIA_FILES.md](./MEDIA_FILES.md).

## Base URL

Use the backend origin as the frontend API base URL, for example
`http://localhost:8000` during local development. Append the endpoint paths
below; do not include `/api/shop` in the base URL if the frontend also appends
it.

All API routes use a trailing slash. The current root URL configuration mounts
the shop API at `/api/shop/`.

## Endpoints

All endpoints are read-only and currently permit unauthenticated requests.
They support `GET` (and standard `HEAD`/`OPTIONS`); create, update, and delete
operations are not available.

| Method | Path | Response |
| --- | --- | --- |
| GET | `/api/shop/product/` | Paginated product list |
| GET | `/api/shop/product/{id}/` | One product by numeric database ID |
| GET | `/api/shop/category/` | Category array |
| GET | `/api/shop/category/{id}/` | One category by numeric database ID |
| GET | `/api/shop/companyconfig/` | Company configuration array |
| GET | `/api/shop/companyconfig/{id}/` | One configuration by numeric database ID |

`slug` is included in product and category data, but detail routes use the
numeric `id`, not the slug.

### Product list pagination

Only the product endpoints are paginated. The page size is 10 and the supported
query parameter is `page`, for example:

```text
GET /api/shop/product/?page=2
```

The response follows DRF's page-number format:

```json
{
  "count": 18,
  "next": "http://localhost:8000/api/shop/product/?page=2",
  "previous": null,
  "results": []
}
```

`next` and `previous` are absolute URLs or `null`. Category and company
configuration list responses are plain JSON arrays, not paginated objects.

## Response fields

### Product

```json
{
  "id": 1,
  "title": "24V 10A Industrial SMPS Switching Power Supply",
  "slug": "24v-10a-industrial-smps-switching-power-supply",
  "sku": "IR-SMPS-2410",
  "category": {
    "id": 1,
    "name": "Power Supplies",
    "slug": "power-supplies",
    "image": "http://localhost:8000/media/cateogry/power-supplies.png",
    "display_order": 1,
    "is_active": true
  },
  "moq": "25 Units",
  "badge": "Bulk Deal",
  "short_description": "Heavy-duty industrial power supply.",
  "images": [
    {
      "id": 41,
      "image": "http://localhost:8000/media/products/2026/11/product-front.png",
      "alt_text": "Front view",
      "sort_order": 0
    },
    {
      "id": 42,
      "image": "http://localhost:8000/media/products/2026/11/product-back.png",
      "alt_text": "Back view",
      "sort_order": 1
    }
  ],
  "specifications": {
    "Input Voltage": "180-264V AC",
    "Output": "24V DC / 10A (240W)"
  },
  "is_featured": true,
  "is_active": true
}
```

The category is nested in each product response. `badge` can be `null` or one
of `"New Arrival"`, `"Bulk Deal"`, `"Trending"`, or `"Best Seller"`.
`specifications` is JSON and its keys depend on each product.

`images` is an array of the product's image records. Each item contains its
database `id`, an `image` URL, optional `alt_text` (empty string when unset),
and `sort_order`. Images are returned by ascending `sort_order`, with ID as a
tie-breaker. An empty array means no product images are available.

### Category

Category objects have these fields:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Database ID |
| `name` | string | Display name |
| `slug` | string | Generated from the name |
| `image` | URL string or `null` | Category image |
| `display_order` | integer | Intended display ordering |
| `is_active` | boolean | The API does not filter inactive categories |

### Company configuration

Company configuration objects have these fields:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Database ID |
| `business_name` | string | |
| `tagline` | string | |
| `logo` | URL string | |
| `favicon` | URL string | |
| `hero_badge_text` | string | |
| `hero_title` | string | |
| `hero_background_image` | URL string | |
| `phone_number` | string | |
| `whatsapp_number` | string | |
| `email` | string | May be empty in seeded data |
| `address` | string or `null` | |
| `map_latitude` | decimal string or `null` | |
| `map_longitude` | decimal string or `null` | |
| `google_maps_embed_url` | string or `null` | |

The endpoint returns an array. The admin interface and sample-data command
currently treat this as a single business configuration, but the API does not
enforce that singleton and the frontend should handle an empty array.

## Images

Image fields on category and company configuration responses are URLs generated
by Django. Product image fields are also URLs. Use those URLs directly as image
sources; do not prepend `/media/` again. For example, a stored category image name
`cateogry/power-supplies.png` is served from
`/media/cateogry/power-supplies.png`.

Images may be hosted on a different origin from the frontend. The backend
currently has no CORS configuration, so browser-side cross-origin API requests
may require CORS to be enabled for the deployed frontend origin. Server-side
Next.js requests are not subject to browser CORS enforcement.

## Filtering and ordering

The API currently has no search, category, active/featured, or ordering query
parameters. Product and category endpoints also do not filter out records
where `is_active` is `false`. The frontend can filter those fields client-side.
`display_order` is provided for categories, but the API does not explicitly
order the queryset; sort by it in the frontend if needed.

## Errors

Standard DRF errors are returned as JSON. A missing detail ID returns HTTP 404,
typically:

```json
{
  "detail": "Not found."
}
```

An invalid or out-of-range product page also returns HTTP 404 with a `detail`
message.

## Local development notes

Run the API from the backend project with Django's development server. The
database settings require the `DEV_POSTGRES_DB_NAME`, `DEV_POSTGRES_USER`,
`DEV_POSTGRES_PASSWORD`, `DEV_POSTGRES_HOST`, and `DEV_POSTGRES_PORT`
environment variables. Sample catalog data can be loaded with:

```text
python manage.py seed_sample_data
```

The seed command creates example business configuration, categories, products,
and product-image records.
