import os
import allure
from allure_commons.types import AttachmentType
import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser tests in headless mode",
    )


@pytest.fixture
def driver(request):
    options = webdriver.FirefoxOptions()
    is_headless = request.config.getoption("--headless") or os.getenv(
        "HEADLESS", "false"
    ).lower() in ("true", "1", "yes")
    if is_headless:
        options.add_argument("-headless")

    driver = webdriver.Firefox(options=options)

    try:
        driver.get("http://localhost:3000")
        driver.delete_all_cookies()
    except Exception:
        pass

    yield driver

    driver.quit()


@pytest.fixture
def authenticated_driver(driver):
    """Provides a driver pre-authenticated via fast API signup & cookie injection."""
    import json
    import urllib.request
    import uuid

    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    payload = json.dumps(
        {"email": email, "password": "testpassword", "name": "Test User"}
    ).encode()

    req = urllib.request.Request(
        "http://localhost:3000/api/auth/sign-up/email",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as response:
        cookie_header = response.headers.get("Set-Cookie", "")
        token = cookie_header.split("better-auth.session_token=")[1].split(";")[0]

    driver.get("http://localhost:3000")
    driver.add_cookie({"name": "better-auth.session_token", "value": token})
    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failure_screenshot",
                attachment_type=AttachmentType.PNG,
            )
