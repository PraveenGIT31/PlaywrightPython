import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
def test_text_input_field(page: Page):
    """Test basic text input functionality"""
    page.goto("https://the-internet.herokuapp.com/inputs")
    
    # Locate input field and enter text
    input_field = page.locator('input[type="number"]')
    input_field.fill("12345")
    
    # Verify the value
    expect(input_field).to_have_value("12345")


@pytest.mark.regression
def test_form_submission(page: Page):
    """Test complete form submission"""
    page.goto("https://the-internet.herokuapp.com/login")
    
    # Fill login form
    page.locator("#username").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")
    
    # Submit form
    page.locator('button[type="submit"]').click()
    
    # Verify successful login
    expect(page.locator(".flash.success")).to_be_visible()
    expect(page.locator(".flash.success")).to_contain_text("You logged into a secure area!")


@pytest.mark.regression
def test_form_validation_errors(page: Page):
    """Test form validation with invalid data"""
    page.goto("https://the-internet.herokuapp.com/login")
    
    # Submit form without credentials
    page.locator('button[type="submit"]').click()
    
    # Verify error message
    expect(page.locator(".flash.error")).to_be_visible()
    expect(page.locator(".flash.error")).to_contain_text("Your username is invalid!")


def test_checkbox_interaction(page: Page):
    """Test checkbox selection and deselection"""
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    
    # Get checkboxes
    checkbox1 = page.locator('input[type="checkbox"]').nth(0)
    checkbox2 = page.locator('input[type="checkbox"]').nth(1)
    
    # Check first checkbox
    checkbox1.check()
    expect(checkbox1).to_be_checked()
    
    # Uncheck second checkbox
    checkbox2.uncheck()
    expect(checkbox2).not_to_be_checked()


def test_dropdown_selection(page: Page):
    """Test dropdown menu selection"""
    page.goto("https://the-internet.herokuapp.com/dropdown")
    
    dropdown = page.locator("#dropdown")
    
    # Select option by value
    dropdown.select_option("1")
    expect(dropdown).to_have_value("1")
    
    # Select option by label
    dropdown.select_option(label="Option 2")
    expect(dropdown).to_have_value("2")


@pytest.mark.smoke
def test_file_upload(page: Page):
    """Test file upload functionality"""
    page.goto("https://the-internet.herokuapp.com/upload")
    
    # Create a test file
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Test file content")
        file_path = f.name
    
    try:
        # Upload file
        page.locator("#file-upload").set_input_files(file_path)
        page.locator("#file-submit").click()
        
        # Verify upload success
        expect(page.locator("h3")).to_have_text("File Uploaded!")
        expect(page.locator("#uploaded-files")).to_contain_text(os.path.basename(file_path))
    finally:
        # Cleanup
        os.unlink(file_path)


def test_radio_button_selection(page: Page):
    """Test radio button selection"""
    page.goto("https://demo.playwright.dev/demo/")
    
    # Note: Using a demo page that has radio buttons
    # Adjust URL and selectors based on actual test requirements
    
    # Example radio button interaction
    # radio_button = page.locator('input[type="radio"][value="option1"]')
    # radio_button.check()
    # expect(radio_button).to_be_checked()
    pass  # Placeholder for actual implementation


@pytest.mark.regression
def test_multi_field_form(page: Page):
    """Test form with multiple field types"""
    page.goto("https://the-internet.herokuapp.com/forgot_password")
    
    # Fill email field
    email_field = page.locator("#email")
    email_field.fill("test@example.com")
    
    # Submit form
    page.locator('button[type="submit"]').click()
    
    # Verify confirmation message
    expect(page.locator("#content")).to_contain_text("Your e-mail's been sent!")


def test_form_field_clearing(page: Page):
    """Test clearing form fields"""
    page.goto("https://the-internet.herokuapp.com/login")
    
    username_field = page.locator("#username")
    
    # Fill and clear
    username_field.fill("testuser")
    expect(username_field).to_have_value("testuser")
    
    username_field.clear()
    expect(username_field).to_be_empty()


@pytest.mark.smoke
def test_form_keyboard_interaction(page: Page):
    """Test form interaction using keyboard"""
    page.goto("https://the-internet.herokuapp.com/login")
    
    # Navigate and fill using keyboard
    page.locator("#username").press_sequentially("tomsmith")
    page.keyboard.press("Tab")
    page.keyboard.type("SuperSecretPassword!")
    page.keyboard.press("Enter")
    
    # Verify successful login
    expect(page.locator(".flash.success")).to_be_visible()