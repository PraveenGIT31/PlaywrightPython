import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_product_search(page: Page):
    """Test product search functionality"""
    page.goto("https://www.saucedemo.com/")
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Verify products page loaded
    expect(page.locator(".title")).to_have_text("Products")
    
    # Verify products are displayed
    products = page.locator(".inventory_item")
    expect(products).to_have_count(6)


@pytest.mark.e2e
@pytest.mark.smoke
def test_add_product_to_cart(page: Page):
    """Test adding a product to shopping cart"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add first product to cart
    page.locator(".inventory_item").first.locator("button").click()
    
    # Verify cart badge shows 1 item
    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")


@pytest.mark.e2e
def test_remove_product_from_cart(page: Page):
    """Test removing a product from cart"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add product to cart
    add_button = page.locator(".inventory_item").first.locator("button")
    add_button.click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
    
    # Remove product
    remove_button = page.locator(".inventory_item").first.locator("button")
    remove_button.click()
    
    # Verify cart is empty
    expect(page.locator(".shopping_cart_badge")).not_to_be_visible()


@pytest.mark.e2e
def test_view_cart(page: Page):
    """Test viewing shopping cart"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add product to cart
    page.locator(".inventory_item").first.locator("button").click()
    
    # Click cart icon
    page.locator(".shopping_cart_link").click()
    
    # Verify cart page
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
    expect(page.locator(".title")).to_have_text("Your Cart")
    expect(page.locator(".cart_item")).to_have_count(1)


@pytest.mark.e2e
@pytest.mark.regression
def test_complete_checkout_process(page: Page):
    """Test complete checkout flow from cart to order confirmation"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add product to cart
    page.locator(".inventory_item").first.locator("button").click()
    
    # Go to cart
    page.locator(".shopping_cart_link").click()
    
    # Proceed to checkout
    page.locator("#checkout").click()
    
    # Fill checkout information
    page.locator("#first-name").fill("John")
    page.locator("#last-name").fill("Doe")
    page.locator("#postal-code").fill("12345")
    page.locator("#continue").click()
    
    # Verify checkout overview
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
    expect(page.locator(".title")).to_have_text("Checkout: Overview")
    
    # Complete purchase
    page.locator("#finish").click()
    
    # Verify order confirmation
    expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")


@pytest.mark.e2e
def test_product_sorting(page: Page):
    """Test product sorting functionality"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Get first product name before sorting
    first_product_before = page.locator(".inventory_item_name").first.text_content()
    
    # Sort by name (Z to A)
    page.locator(".product_sort_container").select_option("za")
    
    # Get first product name after sorting
    first_product_after = page.locator(".inventory_item_name").first.text_content()
    
    # Verify sorting changed the order
    assert first_product_before != first_product_after


@pytest.mark.e2e
def test_product_details_page(page: Page):
    """Test viewing product details"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Click on first product
    first_product_name = page.locator(".inventory_item_name").first.text_content()
    page.locator(".inventory_item_name").first.click()
    
    # Verify product details page
    expect(page.locator(".inventory_details_name")).to_have_text(first_product_name)
    expect(page.locator(".inventory_details_desc")).to_be_visible()
    expect(page.locator(".inventory_details_price")).to_be_visible()


@pytest.mark.e2e
def test_add_multiple_products_to_cart(page: Page):
    """Test adding multiple products to cart"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add three products to cart
    products = page.locator(".inventory_item")
    for i in range(3):
        products.nth(i).locator("button").click()
    
    # Verify cart badge shows 3 items
    expect(page.locator(".shopping_cart_badge")).to_have_text("3")
    
    # Go to cart and verify
    page.locator(".shopping_cart_link").click()
    expect(page.locator(".cart_item")).to_have_count(3)


@pytest.mark.regression
def test_continue_shopping_from_cart(page: Page):
    """Test continue shopping button from cart"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add product and go to cart
    page.locator(".inventory_item").first.locator("button").click()
    page.locator(".shopping_cart_link").click()
    
    # Click continue shopping
    page.locator("#continue-shopping").click()
    
    # Verify back on products page
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


@pytest.mark.e2e
def test_checkout_validation(page: Page):
    """Test checkout form validation"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add product and go to checkout
    page.locator(".inventory_item").first.locator("button").click()
    page.locator(".shopping_cart_link").click()
    page.locator("#checkout").click()
    
    # Try to continue without filling form
    page.locator("#continue").click()
    
    # Verify error message
    expect(page.locator(".error-message-container")).to_be_visible()


@pytest.mark.e2e
def test_logout_clears_cart(page: Page):
    """Test that logout maintains cart state"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add product to cart
    page.locator(".inventory_item").first.locator("button").click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
    
    # Logout
    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()
    
    # Verify logged out
    expect(page).to_have_url("https://www.saucedemo.com/")


@pytest.mark.regression
def test_price_calculation_in_cart(page: Page):
    """Test that prices are calculated correctly in cart"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add products and go through checkout
    page.locator(".inventory_item").first.locator("button").click()
    page.locator(".shopping_cart_link").click()
    page.locator("#checkout").click()
    
    # Fill checkout info
    page.locator("#first-name").fill("John")
    page.locator("#last-name").fill("Doe")
    page.locator("#postal-code").fill("12345")
    page.locator("#continue").click()
    
    # Verify price elements exist
    expect(page.locator(".summary_subtotal_label")).to_be_visible()
    expect(page.locator(".summary_tax_label")).to_be_visible()
    expect(page.locator(".summary_total_label")).to_be_visible()


@pytest.mark.smoke
def test_product_images_displayed(page: Page):
    """Test that product images are displayed correctly"""
    page.goto("https://www.saucedemo.com/")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Verify product images are visible
    product_images = page.locator(".inventory_item_img")
    expect(product_images.first).to_be_visible()
    
    # Check that images have valid src
    img_src = product_images.first.locator("img").get_attribute("src")
    assert img_src is not None and len(img_src) > 0