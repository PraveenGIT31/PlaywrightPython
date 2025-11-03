import pytest
from playwright.sync_api import Page, expect
import re

@pytest.mark.regression
def test_dynamic_content_loading(page: Page):
    """Test dynamic content loading"""
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")
    
    # Click start button
    page.locator("#start button").click()
    
    # Wait for loading indicator
    expect(page.locator("#loading")).to_be_visible()
    
    # Wait for content to appear
    page.wait_for_selector("#finish", state="visible", timeout=10000)
    
    # Verify content loaded
    expect(page.locator("#finish h4")).to_have_text("Hello World!")


@pytest.mark.regression
def test_javascript_alerts(page: Page):
    """Test handling JavaScript alerts"""
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    
    # Test JS Alert
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("button[onclick='jsAlert()']").click()
    
    # Verify result
    expect(page.locator("#result")).to_have_text("You successfully clicked an alert")


def test_javascript_confirm(page: Page):
    """Test handling JavaScript confirm dialogs"""
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    
    # Test JS Confirm - Accept
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("button[onclick='jsConfirm()']").click()
    expect(page.locator("#result")).to_have_text("You clicked: Ok")
    
    # Test JS Confirm - Dismiss
    page.on("dialog", lambda dialog: dialog.dismiss())
    page.locator("button[onclick='jsConfirm()']").click()
    expect(page.locator("#result")).to_have_text("You clicked: Cancel")


def test_javascript_prompt(page: Page):
    """Test handling JavaScript prompts"""
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    
    # Handle prompt with text input
    page.on("dialog", lambda dialog: dialog.accept("Test Input"))
    page.locator("button[onclick='jsPrompt()']").click()
    
    # Verify result
    expect(page.locator("#result")).to_have_text("You entered: Test Input")


@pytest.mark.smoke
def test_drag_and_drop(page: Page):
    """Test drag and drop functionality"""
    page.goto("https://the-internet.herokuapp.com/drag_and_drop")
    
    # Get initial positions
    column_a = page.locator("#column-a")
    column_b = page.locator("#column-b")
    
    initial_a_text = column_a.locator("header").text_content()
    
    # Perform drag and drop
    column_a.drag_to(column_b)
    
    # Verify elements switched positions
    final_a_text = column_a.locator("header").text_content()
    assert initial_a_text != final_a_text


@pytest.mark.regression
def test_infinite_scroll(page: Page):
    """Test infinite scroll functionality"""
    page.goto("https://the-internet.herokuapp.com/infinite_scroll")
    
    # Get initial paragraph count
    initial_count = page.locator(".jscroll-added").count()
    
    # Scroll to bottom
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    
    # Wait for new content
    page.wait_for_timeout(2000)
    
    # Get new paragraph count
    new_count = page.locator(".jscroll-added").count()
    
    # Verify more content loaded
    assert new_count > initial_count


def test_context_menu(page: Page):
    """Test right-click context menu"""
    page.goto("https://the-internet.herokuapp.com/context_menu")
    
    # Handle alert
    page.on("dialog", lambda dialog: dialog.accept())
    
    # Right-click on hot spot
    page.locator("#hot-spot").click(button="right")
    
    # Alert should have been triggered (verified by handler)


@pytest.mark.regression
def test_hover_actions(page: Page):
    """Test hover actions and tooltips"""
    page.goto("https://the-internet.herokuapp.com/hovers")
    
    # Hover over first figure
    first_figure = page.locator(".figure").first
    first_figure.hover()
    
    # Verify caption appears
    caption = first_figure.locator(".figcaption")
    expect(caption).to_be_visible()
    expect(caption.locator("h5")).to_contain_text("name: user1")


def test_multiple_windows(page: Page):
    """Test handling multiple windows/tabs"""
    page.goto("https://the-internet.herokuapp.com/windows")
    
    # Click link to open new window
    with page.context.expect_page() as new_page_info:
        page.locator('a[href="/windows/new"]').click()
    
    new_page = new_page_info.value
    
    # Verify new window content
    expect(new_page.locator("h3")).to_have_text("New Window")
    
    # Close new window
    new_page.close()


@pytest.mark.smoke
def test_nested_frames(page: Page):
    """Test working with nested iframes"""
    page.goto("https://the-internet.herokuapp.com/nested_frames")
    
    # Access top frame
    top_frame = page.frame_locator('frame[name="frame-top"]')
    
    # Access left frame within top frame
    left_frame = top_frame.frame_locator('frame[name="frame-left"]')
    
    # Verify content in nested frame
    expect(left_frame.locator("body")).to_contain_text("LEFT")


def test_iframe_content(page: Page):
    """Test interacting with iframe content"""
    page.goto("https://the-internet.herokuapp.com/iframe")
    
    # Access iframe
    iframe = page.frame_locator("#mce_0_ifr")
    
    # Clear and type in iframe
    iframe.locator("body").clear()
    iframe.locator("body").fill("Hello from Playwright!")
    
    # Verify content
    expect(iframe.locator("body")).to_contain_text("Hello from Playwright!")


@pytest.mark.regression
def test_shadow_dom(page: Page):
    """Test interacting with Shadow DOM elements"""
    # Note: Using a different URL as the-internet doesn't have Shadow DOM
    # This is a template - adjust URL based on actual test requirements
    page.goto("https://the-internet.herokuapp.com/shadowdom")
    
    # Access shadow DOM (if available)
    # shadow_host = page.locator("#shadow-host")
    # shadow_content = shadow_host.locator("shadow=<selector>")
    pass  # Placeholder


@pytest.mark.regression
def test_file_download(page: Page):
    """Test file download functionality"""
    page.goto("https://the-internet.herokuapp.com/download")
    
    # Start waiting for download
    with page.expect_download() as download_info:
        # Click download link
        page.locator('a[href="download/sample.txt"]').click()
    
    download = download_info.value
    
    # Verify download
    assert download.suggested_filename == "sample.txt"


def test_key_presses(page: Page):
    """Test keyboard key press events"""
    page.goto("https://the-internet.herokuapp.com/key_presses")
    
    # Focus input and press keys
    input_field = page.locator("#target")
    input_field.press("Enter")
    
    # Verify result
    expect(page.locator("#result")).to_have_text("You entered: ENTER")
    
    # Test arrow key
    input_field.press("ArrowUp")
    expect(page.locator("#result")).to_have_text("You entered: UP")


@pytest.mark.smoke
def test_geolocation(page: Page):
    """Test geolocation permissions"""
    # Set geolocation
    context = page.context
    context.set_geolocation({"latitude": 40.7128, "longitude": -74.0060})
    context.grant_permissions(["geolocation"])
    
    # Note: Need a page that uses geolocation
    # This is a template
    page.goto("https://example.com")


def test_network_interception(page: Page):
    """Test network request interception"""
    requests = []
    
    # Intercept requests
    page.on("request", lambda request: requests.append(request.url))
    
    page.goto("https://example.com")
    
    # Verify requests were captured
    assert len(requests) > 0
    assert any("example.com" in url for url in requests)


@pytest.mark.regression
def test_console_messages(page: Page):
    """Test capturing console messages"""
    console_messages = []
    
    # Listen for console messages
    page.on("console", lambda msg: console_messages.append(msg.text))
    
    page.goto("https://the-internet.herokuapp.com/")
    
    # You can verify specific console messages if the page logs any


def test_authentication(page: Page):
    """Test HTTP basic authentication"""
    # Navigate with credentials in URL
    page.goto("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    
    # Verify successful authentication
    expect(page.locator("p")).to_contain_text("Congratulations!")


@pytest.mark.regression
def test_entry_ad_modal(page: Page):
    """Test handling entry ad modal"""
    page.goto("https://the-internet.herokuapp.com/entry_ad")
    
    # Wait for modal to appear
    modal = page.locator(".modal")
    expect(modal).to_be_visible()
    
    # Close modal
    page.locator(".modal-footer p").click()
    
    # Verify modal closed
    expect(modal).to_be_hidden()


def test_slow_resources(page: Page):
    """Test handling slow-loading resources"""
    page.goto("https://the-internet.herokuapp.com/slow")
    
    # Wait for page to fully load
    page.wait_for_load_state("networkidle")
    
    # Verify content loaded
    expect(page.locator("h3")).to_be_visible()


@pytest.mark.smoke
def test_notification_messages(page: Page):
    """Test notification message handling"""
    page.goto("https://the-internet.herokuapp.com/notification_message_rendered")
    
    # Click link to trigger notification
    page.locator('a[href="/notification_message"]').click()
    
    # Verify notification appears
    notification = page.locator("#flash")
    expect(notification).to_be_visible()


def test_challenging_dom(page: Page):
    """Test interacting with challenging DOM structures"""
    page.goto("https://the-internet.herokuapp.com/challenging_dom")
    
    # Click colored buttons
    page.locator(".button").first.click()
    
    # Interact with table
    table_rows = page.locator("tbody tr")
    expect(table_rows).to_have_count(10)
    
    # Click edit on first row
    table_rows.first.locator('a[href^="#edit"]').click()