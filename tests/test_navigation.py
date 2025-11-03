import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
def test_basic_navigation(page: Page):
    """Test basic page navigation"""
    page.goto("https://example.com")
    
    # Verify page loaded
    expect(page).to_have_url("https://example.com/")
    expect(page).to_have_title("Example Domain")


def test_link_navigation(page: Page):
    """Test navigation through links"""
    page.goto("https://the-internet.herokuapp.com/")
    
    # Click on a link
    page.locator('a[href="/login"]').click()
    
    # Verify navigation
    expect(page).to_have_url("https://the-internet.herokuapp.com/login")
    expect(page.locator("h2")).to_have_text("Login Page")


@pytest.mark.regression
def test_browser_back_forward(page: Page):
    """Test browser back and forward navigation"""
    # Navigate to first page
    page.goto("https://example.com")
    expect(page).to_have_url("https://example.com/")
    
    # Navigate to second page
    page.goto("https://the-internet.herokuapp.com/")
    expect(page).to_have_url("https://the-internet.herokuapp.com/")
    
    # Go back
    page.go_back()
    expect(page).to_have_url("https://example.com/")
    
    # Go forward
    page.go_forward()
    expect(page).to_have_url("https://the-internet.herokuapp.com/")


def test_page_reload(page: Page):
    """Test page reload functionality"""
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")
    
    # Click start button
    page.locator("#start button").click()
    
    # Wait for content to load
    page.wait_for_selector("#finish", state="visible")
    
    # Reload page
    page.reload()
    
    # Verify page reloaded (content should be hidden again)
    expect(page.locator("#finish")).to_be_hidden()


@pytest.mark.smoke
def test_external_link_opens_new_tab(page: Page):
    """Test external links that open in new tabs"""
    page.goto("https://the-internet.herokuapp.com/")
    
    # Listen for new page
    with page.context.expect_page() as new_page_info:
        # Click link that opens in new tab (if such link exists)
        # This is a placeholder - adjust based on actual page
        pass
    
    # new_page = new_page_info.value
    # expect(new_page).to_have_url("expected_url")


def test_url_parameters(page: Page):
    """Test navigation with URL parameters"""
    page.goto("https://the-internet.herokuapp.com/redirector")
    
    # Verify current URL
    expect(page).to_have_url("https://the-internet.herokuapp.com/redirector")


@pytest.mark.regression
def test_redirect_handling(page: Page):
    """Test automatic redirect handling"""
    page.goto("https://the-internet.herokuapp.com/redirect")
    
    # Click redirect link
    page.locator("#redirect").click()
    
    # Verify redirected to status codes page
    expect(page).to_have_url("https://the-internet.herokuapp.com/status_codes")


def test_hash_navigation(page: Page):
    """Test navigation with hash fragments"""
    page.goto("https://the-internet.herokuapp.com/")
    
    # Navigate to section with hash
    page.goto("https://the-internet.herokuapp.com/#bottom")
    
    # Verify URL contains hash
    expect(page).to_have_url("https://the-internet.herokuapp.com/#bottom")


@pytest.mark.smoke
def test_404_error_page(page: Page):
    """Test handling of 404 error pages"""
    page.goto("https://the-internet.herokuapp.com/status_codes/404")
    
    # Verify error page content
    expect(page.locator("h1")).to_contain_text("Status Codes")


def test_multiple_page_navigation(page: Page):
    """Test navigating through multiple pages in sequence"""
    pages = [
        ("https://the-internet.herokuapp.com/", "Welcome to the-internet"),
        ("https://the-internet.herokuapp.com/login", "Login Page"),
        ("https://the-internet.herokuapp.com/checkboxes", "Checkboxes"),
        ("https://the-internet.herokuapp.com/dropdown", "Dropdown List"),
    ]
    
    for url, expected_heading in pages:
        page.goto(url)
        expect(page).to_have_url(url)
        expect(page.locator("h3, h2")).to_contain_text(expected_heading)


def test_wait_for_navigation(page: Page):
    """Test waiting for navigation to complete"""
    page.goto("https://the-internet.herokuapp.com/")
    
    # Click link and wait for navigation
    with page.expect_navigation():
        page.locator('a[href="/login"]').click()
    
    # Verify navigation completed
    expect(page).to_have_url("https://the-internet.herokuapp.com/login")


@pytest.mark.regression
def test_navigation_timeout_handling(page: Page):
    """Test handling of navigation timeouts"""
    # Set a short timeout
    page.set_default_timeout(5000)
    
    try:
        # Navigate to valid page (should succeed)
        page.goto("https://example.com", wait_until="domcontentloaded")
        expect(page).to_have_url("https://example.com/")
    except Exception as e:
        pytest.fail(f"Navigation failed: {str(e)}")


def test_base_url_navigation(page: Page):
    """Test relative URL navigation"""
    page.goto("https://the-internet.herokuapp.com/")
    
    # Navigate using relative path
    page.goto("login")
    
    # Verify navigation
    expect(page).to_have_url("https://the-internet.herokuapp.com/login")


@pytest.mark.e2e
def test_complex_navigation_flow(page: Page):
    """Test complex multi-step navigation flow"""
    # Start at home
    page.goto("https://the-internet.herokuapp.com/")
    expect(page.locator("h1")).to_contain_text("Welcome")
    
    # Navigate to login
    page.locator('a[href="/login"]').click()
    expect(page).to_have_url("https://the-internet.herokuapp.com/login")
    
    # Perform login
    page.locator("#username").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")
    page.locator('button[type="submit"]').click()
    
    # Verify secure area
    expect(page).to_have_url("https://the-internet.herokuapp.com/secure")
    expect(page.locator("h2")).to_have_text(" Secure Area")
    
    # Logout
    page.locator('a[href="/logout"]').click()
    
    # Verify back at login
    expect(page).to_have_url("https://the-internet.herokuapp.com/login")


def test_javascript_navigation(page: Page):
    """Test navigation triggered by JavaScript"""
    page.goto("https://the-internet.herokuapp.com/")
    
    # Execute JavaScript to navigate
    page.evaluate("window.location.href = '/login'")
    
    # Verify navigation
    expect(page).to_have_url("https://the-internet.herokuapp.com/login")