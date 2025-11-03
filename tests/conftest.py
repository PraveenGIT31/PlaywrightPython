import pytest

@pytest.fixture(scope="session")
def setup_playwright():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        yield p

@pytest.fixture(autouse=True)
def setup_page(setup_playwright):
    # This fixture will run before each test
    browser = setup_playwright.chromium.launch()
    page = browser.new_page()
    yield page
    page.close()
    browser.close()