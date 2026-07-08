from playwright.sync_api import Page, expect

class LoginOut:

    def __init__(self, page: Page):

        self.page = page
        self.profile_menu_button = page.locator("span.oxd-userdropdown-tab")
        self.logout_button = page.get_by_role("menuitem", name="Logout", exact=True)

    def click_profile_menu(self):
        try:
            self.profile_menu_button.click()
            print("[PASS]Profile menu button clicked successfully.")
        except Exception as e:
            print(f"Error clicking profile menu button: {e}")

    def click_logout(self):
        try:
            self.logout_button.click()
            print("[PASS]Logout button clicked successfully.")
        except Exception as e:
            print(f"Error clicking logout button: {e}")