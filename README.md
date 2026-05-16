# ecommerce_web

A **Django 5.0** based e‑commerce web application featuring:

- User authentication (signup / login / logout)
- Product catalog with categories and images
- Shopping cart with quantity controls
- **Checkout page** that captures shipping address, phone number and supports **Cash on Delivery**
- Order history page displaying past orders with expandable details
- Responsive UI built with custom CSS variables (`--orange`, `--black`, etc.)

## Design improvements

- **Checkout page** now has a modern two‑column layout, larger typography, highlighted form fields and a clear order‑summary card.
- **Orders page** mirrors the checkout styling: cards with orange accents, toggleable item lists, and responsive adjustments for mobile devices.
- Dedicated CSS files `checkout.css` and `orders.css` keep styling modular and maintainable.

## Quick start

1. **Clone the repo** and navigate to the project root:
   ```bash
   git clone <repo-url>
   cd ecommerce_web
   ```
2. **Create a virtual environment** and install dependencies:
   ```bash
   python -m venv env
   source env/bin/activate   # on Windows use `env\Scripts\activate`
   pip install -r requirements.txt
   ```
3. **Apply migrations** (including the new `address`, `phone`, and `payment_method` fields on `Order`):
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```
6. Open your browser at `http://127.0.0.1:8000/app/` and explore the store.

## Project structure
```
 ecommerce_app/      # Django project settings
 └─ store/           # Main app (models, views, templates, static)
     ├─ models.py
     ├─ views.py
     ├─ templates/   # includes `checkout.html` and `orders.html`
     └─ static/      # CSS files: `style.css`, `checkout.css`, `orders.css`
```

## License

MIT – feel free to fork, modify and extend.

