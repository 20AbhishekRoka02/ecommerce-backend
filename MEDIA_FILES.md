# Media files

Django stores uploaded images relative to `MEDIA_ROOT`. `MEDIA_URL` provides
the public URL prefix, so a stored name such as
`cateogry/sensors-modules.png` is served from
`/media/cateogry/sensors-modules.png`.

Category images are stored under `cateogry/`, business images under `assets/`,
and product images under `products/YYYY/MM/`. These names intentionally do not
include `media/`; `MEDIA_URL` already supplies that prefix.

## Render persistent disk

For a Render deployment using local media storage:

1. Attach a persistent disk to the web service, mounted at `/var/data`.
2. Set the service environment variable `MEDIA_ROOT` to `/var/data`.
3. Copy the existing contents of the project's `media/` directory to the root
   of that disk, preserving the `assets/` and `cateogry/` subdirectories.
4. Run Django migrations during deployment so existing stored image names have
   the redundant `media/` prefix removed.

The backend serves public media files from the configured `MEDIA_ROOT`. This
keeps the setup simple for the current project; a higher-traffic deployment
should move media delivery to dedicated object storage/CDN.
