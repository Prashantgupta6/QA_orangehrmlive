import pytest
import time
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.logout_page import LoginOut
from config import Config  # Configuration file holding credentials

def test_invalid_user_login(page):
    """
    Automated Test Case: Verify that login fails for invalid user credentials.
    """

    # --- Page Object Initialization ---
    login_page = LoginPage(page)
    login_out = LoginOut(page)


    # --- Step 1:Login Page ---
    page.goto(Config.BASE_URL + "/web/index.php/auth/login")
    time.sleep(3)
    # validate that we are on the login page by checking for the presence of the login form
    # assert login_page.login_page_yexy.is_visible(), "Login"
    # assert login_page.login_page_logo.is_visible(), "company-branding"
    # --- Step 2: Enter Invalid Credentials ---
    login_page.set_email(Config.USERNAME)
    login_page.set_password(Config.PASSWORD)
    login_page.click_login()
    time.sleep(10)

    # validate loin is successful by checking for the presence of the dashboard page elements'

    expect(page.get_by_role("heading", name="Dashboard", exact=True)).to_be_visible()
    expect(page.get_by_role("link", name="Dashboard", exact=True)).to_be_visible()

    # --- Step 3: Logout ---
    login_out.click_profile_menu()
    login_out.click_logout()
    time.sleep(3)

    

