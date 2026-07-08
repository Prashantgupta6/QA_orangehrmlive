class Config:
    BASE_URL = "https://opensource-demo.orangehrmlive.com"
    LOGIN_URL = f"{BASE_URL}/web/index.php/auth/login"
    DASHBOARD_URL = f"{BASE_URL}/web/index.php/dashboard/index"

    USERNAME = "Admin"
    PASSWORD = "admin123"

    invalid_email = "invalid_user"
    invalid_password = "wrong_password"
