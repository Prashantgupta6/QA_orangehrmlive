import time
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

from config import Config
from pages.login_page import LoginPage
from pages.logout_page import LoginOut

# ========================================================================
# PYTEST + PLAYWRIGHT CONFIGURATION
# ========================================================================
# Browser/context/page fixtures and the --browser/--headed/--screenshot/
# --video/--tracing/--output CLI options all come from the pytest-playwright
# plugin (configured via pytest.ini) - they are not redefined here, since
# redeclaring them would conflict with the plugin's own option strings and
# spin up a second, disconnected browser.
#
# This file adds:
# 1. authenticated_page - suite-level login/logout fixture
# 2. A hook to attach a screenshot to the Allure report on failure
# 3. A fixture to recreate the reports/allure-results dirs, since
#    pytest-playwright's autouse "delete_output_dir" fixture rmtree's the
#    --output dir at session start and never recreates it, which otherwise
#    crashes allure-pytest / pytest-html trying to write into it.
# ========================================================================


@pytest.fixture(scope="session", autouse=True)
def _ensure_report_dirs(delete_output_dir, pytestconfig):
    Path(pytestconfig.getoption("--output")).mkdir(parents=True, exist_ok=True)
    alluredir = pytestconfig.getoption("--alluredir")
    if alluredir:
        Path(alluredir).mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def authenticated_page(browser):
    """
    Suite-level setup/teardown.
    Setup:    log in once before any test in the suite runs.
    Teardown: log out once after all tests in the suite have run.
    """
    context = browser.new_context()
    page = context.new_page()

    # --- Setup: Login ---
    login_page = LoginPage(page)
    page.goto(Config.LOGIN_URL)
    time.sleep(3)
    login_page.set_email(Config.USERNAME)
    login_page.set_password(Config.PASSWORD)
    login_page.click_login()
    time.sleep(10)
    expect(page.get_by_role("heading", name="Dashboard", exact=True)).to_be_visible()

    yield page

    # --- Teardown: Logout ---
    login_out = LoginOut(page)
    login_out.click_profile_menu()
    login_out.click_logout()
    time.sleep(3)

    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Track pass/fail per test phase, and attach a screenshot to the Allure
    report when the test body fails. Runs during the "call" phase, before
    fixture teardown, so whichever Page fixture the test used (page or
    authenticated_page) is still open.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        page = next((v for v in item.funcargs.values() if isinstance(v, Page)), None)
        if page is not None:
            try:
                allure.attach(
                    page.screenshot(),
                    name=f"{item.name}-failure",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as e:
                print(f"[WARN] Could not attach failure screenshot to Allure: {e}")
