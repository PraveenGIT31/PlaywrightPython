# PlaywrightPython

A comprehensive Playwright Python testing framework with pytest integration for automated web testing.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Test Markers](#test-markers)
- [Writing Tests](#writing-tests)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This framework provides a robust foundation for automated browser testing using Playwright with Python. It includes pre-configured pytest settings, reusable fixtures, and example test scenarios covering common web testing patterns.

## ✨ Features

- ✅ Playwright integration with pytest
- ✅ Support for multiple browsers (Chromium, Firefox, WebKit)
- ✅ Configurable test execution modes (headed/headless)
- ✅ Custom test markers for test organization
- ✅ Page fixtures with automatic cleanup
- ✅ Screenshot capture on test failures
- ✅ Comprehensive example test scenarios

## 📦 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/PraveenGIT31/PlaywrightPython.git
cd PlaywrightPython
```

### 2. Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install
```

Or install specific browsers:

```bash
playwright install chromium
playwright install firefox
playwright install webkit
```

## 📁 Project Structure

```
PlaywrightPython/
├── tests/
│   ├── conftest.py           # Pytest fixtures and configuration
│   ├── test_example.py       # Basic example tests
│   ├── test_forms.py         # Form interaction tests
│   ├── test_navigation.py    # Navigation and routing tests
│   └── test_ecommerce.py     # E-commerce scenario tests
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🧪 Running Tests

### Run all tests

```bash
pytest
```

### Run tests in headless mode

```bash
pytest --headless
```

### Run tests in headed mode (see browser)

```bash
pytest --headed
```

### Run specific test file

```bash
pytest tests/test_example.py
```

### Run specific test function

```bash
pytest tests/test_example.py::test_example
```

### Run tests with verbose output

```bash
pytest -v
```

### Run tests and show print statements

```bash
pytest -s
```

## 🏷️ Test Markers

Organize and run tests using custom markers:

### Run smoke tests

```bash
pytest -m smoke
```

### Run regression tests

```bash
pytest -m regression
```

### Run end-to-end tests

```bash
pytest -m e2e
```

### Run multiple markers

```bash
pytest -m "smoke or regression"
```

### Exclude specific markers

```bash
pytest -m "not e2e"
```

## ✍️ Writing Tests

### Basic test structure

```python
import pytest
from playwright.sync_api import Page, expect

def test_my_feature(page: Page):
    # Navigate to page
    page.goto("https://example.com")
    
    # Interact with elements
    page.locator("#my-button").click()
    
    # Assert expectations
    expect(page.locator(".result")).to_have_text("Success")
```

### Using test markers

```python
@pytest.mark.smoke
def test_critical_feature(page: Page):
    # Your test code here
    pass

@pytest.mark.regression
@pytest.mark.e2e
def test_full_workflow(page: Page):
    # Your test code here
    pass
```

## ⚙️ Configuration

### pytest.ini

The `pytest.ini` file contains default configuration:

- **Headed mode by default**: Tests run with visible browser
- **Verbose output**: Detailed test execution information
- **Show print statements**: Console output is displayed
- **Test discovery**: Automatically finds test files matching `test_*.py`

### Modify test execution

Edit `pytest.ini` to change default behavior:

```ini
[pytest]
addopts = -v -s --headless  # Change to headless
```

## 🎯 Best Practices

1. **Use descriptive test names**: `test_user_can_login_successfully`
2. **One assertion per test**: Keep tests focused and simple
3. **Use Page Object Model**: For complex applications, implement POM pattern
4. **Clean up after tests**: Use fixtures to ensure proper cleanup
5. **Use explicit waits**: Leverage Playwright's auto-waiting features
6. **Capture screenshots**: On failures for easier debugging
7. **Use markers**: Organize tests for different test suites

## 🐛 Troubleshooting

### Browsers not installed

```bash
playwright install
```

### Tests running too slow

- Run in headless mode: `pytest --headless`
- Reduce parallel execution if using pytest-xdist

### Element not found errors

- Check selectors are correct
- Ensure page has loaded before interacting
- Use `page.wait_for_selector()` for dynamic content

### Port already in use

- Close other browser instances
- Change default port in configuration

## 📚 Additional Resources

- [Playwright Python Documentation](https://playwright.dev/python/docs/intro)
- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Best Practices](https://playwright.dev/python/docs/best-practices)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Praveen**

- GitHub: [@PraveenGIT31](https://github.com/PraveenGIT31)

---

**Happy Testing! 🚀**
