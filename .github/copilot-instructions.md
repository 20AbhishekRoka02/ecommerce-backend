# Repository guidance

## Stack and entry points

- Django 5.2 REST API using Django REST Framework.
- The only Django application is `shop`; project configuration is in `backend/`.
- Start at `manage.py` for Django commands.
- PostgreSQL is the configured database. The Docker Compose stack also provides Adminer on port 8080.
- The API is rooted at `/api/shop/`; Django admin is at `/admin/`.
- Python 3.11 is used by the Docker image.

## Build and run

Install dependencies locally with:

```powershell
python -m pip install -r requirements.txt
```

Build and start the full stack:

```powershell
docker compose up --build
```

The app is available on port 8000. Django database variables are supplied through `.env` and `compose.yaml`:

- `DEV_POSTGRES_DB_NAME`
- `DEV_POSTGRES_USER`
- `DEV_POSTGRES_PASSWORD`
- `DEV_POSTGRES_HOST`
- `DEV_POSTGRES_PORT`

Keep the PostgreSQL password in `.env` aligned with the `POSTGRES_PASSWORD` used by the `db` service.

Run Django commands in the app container:

```powershell
docker compose exec app python manage.py migrate
docker compose exec app python manage.py makemigrations shop
docker compose exec app python manage.py createsuperuser
docker compose exec app python manage.py shell
docker compose exec app python manage.py check
docker compose exec app python manage.py runserver 0.0.0.0:8000
```

## Tests

Tests use Django's test runner (`shop/tests.py` is present but currently contains no tests).

Run the shop test suite:

```powershell
docker compose exec app python manage.py test shop
```

Run a single test module, class, or method:

```powershell
docker compose exec app python manage.py test shop.tests.TestClass
docker compose exec app python manage.py test shop.tests.TestClass.test_method
```

For local execution, replace `docker compose exec app ` with `python `; database environment variables must be available.

No formatter, linter, pytest configuration, or separate lint command is present. Use `python manage.py check` as the repository's Django validation command.

## Architecture

- `backend/settings.py` configures installed apps, PostgreSQL, Django REST Framework, and page-size pagination of 10 items.
- `backend/urls.py` mounts the Django admin at `/admin/` and the shop router at `/api/shop/`.
- `shop/models.py` contains the domain models:
  - `CompanyConfig` stores singleton-style business and storefront configuration.
  - `Category` and `Product` form the catalog hierarchy.
  - `ProductImage` stores ordered gallery images for a product.
- `shop/serializers.py` uses DRF `ModelSerializer` classes. `ProductSerializer` embeds `CategorySerializer`; `CompanyConfigSerializer` and `CategorySerializer` expose model fields directly.
- `shop/views.py` exposes read-only model viewsets with DRF pagination.
- `shop/urls.py` registers `product`, `category`, and `companyconfig` resources with a `SimpleRouter`.
- `shop/admin.py` registers the catalog models and prevents deleting or creating additional `CompanyConfig` records.

## Conventions

- Add product/catalog API behavior consistently across model, migration, serializer, viewset, and shop router code.
- Keep API resources read-only unless the endpoint requirements explicitly change the viewsets.
- Preserve the `category` nesting in `ProductSerializer` unless a deliberate API shape change is intended.
- Use Django migrations for model changes:
  - `python manage.py makemigrations shop`
  - `python manage.py migrate`
- Keep Django REST Framework's pagination behavior in mind: collections are paginated with 10 records per page unless a view explicitly changes its pagination class.
- Update `shop/admin.py` for fields or relationships that need to be managed through Django admin.
- Company configuration is treated as a singleton in admin; do not remove the existing add/delete guards casually.
