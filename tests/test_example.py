import pytest
from playwright.sync_api import Page, expect

def test_example(page: Page):
    # Navigate to the website
    page.goto("https://example.com")
    
    # Expect a title "to contain" a substring.
    expect(page).to_have_title("Example Domain")
    
    # Expect an element "to be visible".
    expect(page.locator("h1")).to_be_visible()
    
    # Click the element.
    page.locator("h1").click()
    
    # Assert that the text content is correct.
    expect(page.locator("h1")).to_have_text("Example Domain")