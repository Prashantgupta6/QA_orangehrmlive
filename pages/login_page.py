from playwright.sync_api import Page, expect

class LoginPage:

    def __init__(self, page: Page):

        self.page = page
        self.login_page_logo = page.get_by_alt_text("company-branding")
        self.login_page_yexy = page.get_by_role("heading", name="Login", exact=True)
        self.login_email_input = page.get_by_placeholder("Username", exact=True)
        self.login_password_input = page.get_by_placeholder("Password", exact=True)
        self.login_button = page.get_by_role("button", name="Login", exact=True)

    def set_email(self, email: str):
        try:
            self.login_email_input.fill(email)
            print("[PASS]Email set successfully.")
        except Exception as e:
            print(f"Error setting email: {e}")

    def set_password(self, password: str):
        try:
            self.login_password_input.fill(password)
            print("[PASS]Password set successfully.")
        except Exception as e:
            print(f"Error setting password: {e}")

    def click_login(self):
        try:
            self.login_button.click()
            print("[PASS]Login button clicked successfully.")
        except Exception as e:
            print(f"Error clicking login button: {e}")