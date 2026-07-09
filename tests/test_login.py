import pytest
from playwright.sync_api import expect


@pytest.mark.sanity
def test_dashboard_visible(authenticated_page):
    """
    Verify the dashboard is visible after suite-level login (see conftest.authenticated_page).
    """
    expect(authenticated_page.get_by_role("link", name="Dashboard", exact=True)).to_be_visible()
