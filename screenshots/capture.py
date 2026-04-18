"""
Screenshot Capture Module for StyleVault Assignment
Uses Selenium WebDriver to capture website screenshots for the report.
"""

import os
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'screenshots')
BASE_URL = 'http://127.0.0.1:5000'


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_driver():
    """Configure and return a headless Chrome WebDriver."""
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1400,900')
    options.add_argument('--disable-gpu')
    options.add_argument('--force-device-scale-factor=1')

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception:
        # Fallback: try system Chrome
        driver = webdriver.Chrome(options=options)

    return driver


def capture_page(driver, path, filename, wait_time=2):
    """Navigate to a URL and capture a screenshot."""
    url = f'{BASE_URL}{path}'
    driver.get(url)
    time.sleep(wait_time)
    filepath = os.path.join(OUTPUT_DIR, filename)
    driver.save_screenshot(filepath)
    print(f"[SCREENSHOT] Saved: {filename}")
    return filepath


def logout_user(driver):
    """Log out the current user by visiting /logout."""
    driver.get(f'{BASE_URL}/logout')
    time.sleep(1.5)
    print("[SCREENSHOT] Logged out.")


def login_user(driver, email='demo@stylevault.com', password='Demo123!', label='demo user'):
    """Log in a user via the login form — targets the login form specifically."""
    driver.get(f'{BASE_URL}/login')
    time.sleep(1.5)

    # If already logged in, Flask redirects /login → /; logout first
    if '/login' not in driver.current_url:
        logout_user(driver)
        driver.get(f'{BASE_URL}/login')
        time.sleep(1.5)

    # Fill the login form fields (not the navbar search)
    login_form = driver.find_element(By.CSS_SELECTOR, 'form[action*="login"]')
    email_field = login_form.find_element(By.NAME, 'email')
    pass_field  = login_form.find_element(By.NAME, 'password')
    email_field.clear()
    email_field.send_keys(email)
    pass_field.clear()
    pass_field.send_keys(password)

    # Click the submit button WITHIN the login form only
    submit_btn = login_form.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit_btn.click()
    time.sleep(2.5)
    print(f"[SCREENSHOT] Logged in as {label}.")


def login_admin(driver):
    """Log out current user then log in as admin for admin page screenshots."""
    logout_user(driver)
    login_user(driver, email='admin@stylevault.com', password='Admin123!', label='admin')


def add_item_to_cart(driver, slug='silk-midi-dress'):
    """Add a product to the cart — targets the add-to-cart form specifically."""
    driver.get(f'{BASE_URL}/product/{slug}')
    time.sleep(1.5)

    try:
        # Find the add-to-cart form by its action URL
        cart_form = driver.find_element(By.CSS_SELECTOR, 'form[action*="cart/add"]')
        size_select = cart_form.find_element(By.NAME, 'size')
        size_select.click()
        time.sleep(0.3)
        from selenium.webdriver.support.ui import Select
        Select(size_select).select_by_index(1)

        # Click the Add to Cart button (first button in the form)
        add_btn = cart_form.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        add_btn.click()
        time.sleep(2)
        print(f"[SCREENSHOT] Item added to cart: {slug}.")
    except Exception as e:
        print(f"[SCREENSHOT] Warning: Could not add to cart: {e}")


def capture_all_screenshots():
    """Capture all required screenshots for the report."""
    ensure_output_dir()
    print("\n" + "="*60)
    print("  CAPTURING WEBSITE SCREENSHOTS")
    print("="*60)

    driver = get_driver()
    paths = {}

    try:
        # ── Public pages ────────────────────────────────────
        paths['homepage'] = capture_page(driver, '/', 'homepage.png')
        paths['products_women'] = capture_page(driver, '/collection/women', 'products_women.png')
        paths['products_men'] = capture_page(driver, '/collection/men', 'products_men.png')
        paths['products_accessories'] = capture_page(driver, '/collection/accessories', 'products_accessories.png')
        paths['product_detail'] = capture_page(driver, '/product/silk-midi-dress', 'product_detail.png')
        paths['contact'] = capture_page(driver, '/contact', 'contact_page.png')
        paths['about'] = capture_page(driver, '/about', 'about_page.png')

        # ── Auth pages ──────────────────────────────────────
        paths['login'] = capture_page(driver, '/login', 'login_page.png')
        paths['register'] = capture_page(driver, '/register', 'register_page.png')

        # ── Search & Filter pages ───────────────────────────
        paths['search_results'] = capture_page(driver, '/search?q=dress', 'search_results.png')
        paths['filtered_price'] = capture_page(driver, '/collection?min_price=100&max_price=400&sort=price_low', 'filtered_products.png')
        paths['sorted_products'] = capture_page(driver, '/collection?sort=price_high', 'sorted_products.png')

        # ── Sale / Men product detail ────────────────────────
        paths['product_detail_men'] = capture_page(driver, '/product/italian-wool-suit', 'product_detail_men.png')
        paths['product_detail_sale'] = capture_page(driver, '/product/cotton-polo-shirt', 'product_detail_sale.png')

        # ── Homepage scrolled (features + promo) ────────────
        driver.get(f'{BASE_URL}/')
        time.sleep(1.5)
        driver.execute_script("window.scrollTo(0, 700)")
        time.sleep(0.8)
        fp = os.path.join(OUTPUT_DIR, 'homepage_new_arrivals.png')
        driver.save_screenshot(fp)
        paths['homepage_new_arrivals'] = fp
        print("[SCREENSHOT] Saved: homepage_new_arrivals.png")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.8)
        fp = os.path.join(OUTPUT_DIR, 'homepage_footer.png')
        driver.save_screenshot(fp)
        paths['homepage_footer'] = fp
        print("[SCREENSHOT] Saved: homepage_footer.png")

        # ── Logged-in pages ─────────────────────────────────
        login_user(driver)
        paths['homepage_loggedin'] = capture_page(driver, '/', 'homepage_loggedin.png')

        # Product detail page with cart button visible
        paths['product_detail_loggedin'] = capture_page(
            driver, '/product/leather-chelsea-boots', 'product_detail_loggedin.png')

        # Hover over product listing to show quick-add (JS injection)
        driver.get(f'{BASE_URL}/collection/women')
        time.sleep(1.5)
        try:
            driver.execute_script(
                "document.querySelector('.quick-add-overlay').style.transform='translateY(0)';")
            time.sleep(0.5)
        except Exception:
            pass
        fp = os.path.join(OUTPUT_DIR, 'product_listing_quickadd.png')
        driver.save_screenshot(fp)
        paths['product_listing_quickadd'] = fp
        print("[SCREENSHOT] Saved: product_listing_quickadd.png")

        # Add product and capture cart
        add_item_to_cart(driver)

        # Add a second product to show multi-item cart
        add_item_to_cart(driver, 'leather-chelsea-boots')

        paths['cart'] = capture_page(driver, '/cart', 'cart_page.png')

        # Cart scrolled to order summary
        driver.get(f'{BASE_URL}/cart')
        time.sleep(1.5)
        driver.execute_script("window.scrollTo(0, 300)")
        time.sleep(0.5)
        fp = os.path.join(OUTPUT_DIR, 'cart_summary.png')
        driver.save_screenshot(fp)
        paths['cart_summary'] = fp
        print("[SCREENSHOT] Saved: cart_summary.png")

        paths['checkout'] = capture_page(driver, '/checkout', 'checkout_page.png')

        # Checkout page scrolled to form
        driver.get(f'{BASE_URL}/checkout')
        time.sleep(1.5)
        driver.execute_script("window.scrollTo(0, 300)")
        time.sleep(0.5)
        fp = os.path.join(OUTPUT_DIR, 'checkout_form.png')
        driver.save_screenshot(fp)
        paths['checkout_form'] = fp
        print("[SCREENSHOT] Saved: checkout_form.png")

        # ── Admin pages — must log in as admin first ─────────────
        print("[SCREENSHOT] Logging in as admin for admin screenshots...")
        login_admin(driver)

        # Admin dashboard
        paths['admin_dashboard'] = capture_page(driver, '/admin', 'admin_dashboard.png', wait_time=2)

        # Admin dashboard scrolled (orders + inventory tables)
        driver.get(f'{BASE_URL}/admin')
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 400)")
        time.sleep(0.8)
        fp = os.path.join(OUTPUT_DIR, 'admin_dashboard_tables.png')
        driver.save_screenshot(fp)
        paths['admin_dashboard_tables'] = fp
        print("[SCREENSHOT] Saved: admin_dashboard_tables.png")

        # ── Admin CRUD pages ─────────────────────────────────────
        print("[SCREENSHOT] Capturing admin CRUD pages...")

        # Admin analytics
        paths['admin_analytics'] = capture_page(driver, '/admin/analytics', 'admin_analytics.png', wait_time=2)

        # Admin analytics scrolled to tables
        driver.get(f'{BASE_URL}/admin/analytics')
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 400)")
        time.sleep(0.8)
        fp = os.path.join(OUTPUT_DIR, 'admin_analytics_tables.png')
        driver.save_screenshot(fp)
        paths['admin_analytics_tables'] = fp
        print("[SCREENSHOT] Saved: admin_analytics_tables.png")

        # Admin product management list
        paths['admin_products_list'] = capture_page(driver, '/admin/products', 'admin_products_list.png', wait_time=2)

        # Admin add product form
        paths['admin_add_product'] = capture_page(driver, '/admin/products/add', 'admin_add_product.png', wait_time=2)

        # Admin edit product (first product)
        paths['admin_edit_product'] = capture_page(driver, '/admin/products/1/edit', 'admin_edit_product.png', wait_time=2)

        # ── Responsiveness screenshots ──────────────────────────
        print("[SCREENSHOT] Capturing responsive design screenshots...")

        # Mobile view (375px - iPhone SE)
        driver.set_window_size(375, 812)
        time.sleep(0.5)
        paths['mobile_homepage'] = capture_page(driver, '/', 'responsive_mobile_homepage.png', wait_time=1.5)

        driver.set_window_size(375, 812)
        paths['mobile_products'] = capture_page(driver, '/collection/women', 'responsive_mobile_products.png', wait_time=1.5)

        driver.set_window_size(375, 812)
        paths['mobile_nav'] = capture_page(driver, '/', 'responsive_mobile_nav.png', wait_time=1)
        try:
            driver.find_element(By.CSS_SELECTOR, '.navbar-toggler').click()
            time.sleep(0.5)
            fp = os.path.join(OUTPUT_DIR, 'responsive_mobile_menu.png')
            driver.save_screenshot(fp)
            paths['mobile_menu'] = fp
            print("[SCREENSHOT] Saved: responsive_mobile_menu.png")
        except Exception:
            pass

        # Tablet view (768px - iPad)
        driver.set_window_size(768, 1024)
        time.sleep(0.5)
        paths['tablet_homepage'] = capture_page(driver, '/', 'responsive_tablet_homepage.png', wait_time=1.5)
        paths['tablet_products'] = capture_page(driver, '/collection/women', 'responsive_tablet_products.png', wait_time=1.5)

        # Restore desktop size
        driver.set_window_size(1400, 900)
        time.sleep(0.3)

        print(f"\n[DONE] Captured {len(paths)} screenshots successfully.")

    except Exception as e:
        print(f"[ERROR] Screenshot capture failed: {e}")
    finally:
        driver.quit()

    return paths


def start_flask_server():
    """Start the Flask server in a separate thread."""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'website'))

    from app import create_app
    from models import db

    app = create_app()
    with app.app_context():
        db.create_all()
        if not db.session.execute(db.select(db.Model.metadata.tables.get('products', None) or db.text("SELECT 1"))).first():
            from seed_data import seed_database
            seed_database(db)

    def run():
        app.run(port=5000, debug=False, use_reloader=False)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    time.sleep(3)  # Wait for server to start
    return thread


if __name__ == '__main__':
    start_flask_server()
    capture_all_screenshots()
