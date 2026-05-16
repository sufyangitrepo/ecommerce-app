# AGENTS.md

## Project Structure

**Django 5.0 e-commerce application** with a monolithic structure:
- Root: `/ecommerce_web/` (workspace)
- App code: `/ecommerce_web/ecommerce_app/` (Django project + app)
- Single app: `store/` (models, views, templates, static)
- Database: SQLite (`db.sqlite3` in project root)
- Virtual environment: `/ecommerce_web/env/`

## Essential Commands

All commands run from `/ecommerce_web/ecommerce_app/`:

| Task | Command |
|------|---------|
| Run dev server | `python manage.py runserver` |
| Create migrations | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |
| Create superuser | `python manage.py createsuperuser` |
| Run tests | `python manage.py test` |
| Shell | `python manage.py shell` |
| Collect static | `python manage.py collectstatic --noinput` |

## Key Locations

- Settings: `ecommerce_app/settings.py` — Django config, installed apps, database setup
- Models: `store/models.py` — Category, Product, Cart, Order, Rating
- Views: `store/views.py` — 10 views (signup, login, logout, products, cart, orders, search)
- URLs: `store/urls.py` — route definitions
- Templates: `store/templates/` — HTML templates for all views
- Static: `store/static/` — CSS, JS, images
- Media: `/media/` — user-uploaded images (Category and Product)

## Dependencies

- Django (5.0)
- Pillow (image handling for `ImageField`)
- asgiref, sqlparse (Django dependencies)

See `requirements.txt` for full list.

## Important Notes

### Media Handling
- Images upload to `/media/assets/images/`
- `MEDIA_URL = '/media/'` and `MEDIA_ROOT` configured in settings
- Category and Product models use `ImageField`

### Authentication
- Uses Django's built-in `User` model and auth system
- User-based cart and order tracking (ForeignKey to User)
- Login check: `request.user.is_anonymous`

### Database Schema
- **Cart**: per-user (one per User), stores total
- **CartItem**: individual items in cart (qty, amount)
- **Order**: completed orders (user, total_price, **address**, **phone**, **payment_method**)
- **OrderItem**: items in order (mirrors CartItem structure)
- **Rating**: product ratings by user (1–5 decimal)

## New Features & UI Improvements
- **Checkout page** now includes a modern two‑column layout with larger typography, highlighted input fields for shipping address and phone number, and a read‑only Cash on Delivery payment method.
- **Orders page** displays past orders in card format, with expandable item lists and responsive design.
- Dedicated CSS files `checkout.css` and `orders.css` keep styling modular and maintainable.



### Common Issues
- **image uploads**: Ensure `MEDIA_ROOT` directory exists and is writable
- **templates**: Looks for templates in `store/templates/` and root `templates/` dir (see settings.py line 59)
- **migrations**: Run `makemigrations` then `migrate` after model changes; check `store/migrations/` for history
- **debug mode**: `DEBUG = True` in settings (development only; never in production)

## Testing
- Test file: `store/tests.py` (currently minimal/empty)
- Run: `python manage.py test store` (test store app only) or `python manage.py test` (all)
- No external test runners (pytest, tox) configured

## Deployment Notes
- `SECRET_KEY` hardcoded in settings.py (security risk—use environment variables in production)
- `ALLOWED_HOSTS = ['*']` (too permissive—restrict in production)
- Static files: run `collectstatic` before serving
