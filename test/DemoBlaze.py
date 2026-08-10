import sys
from pathlib import Path

from playwright.sync_api import Playwright, sync_playwright

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pages.home_page import HomePage


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    home_page = HomePage(page)
    home_page.open()
    home_page.login("Nagarajanvn", "Password12345")

    product_page = home_page.open_product("MacBook Pro")
    product_page.add_to_cart()

    cart_page = product_page.open_cart()
    cart_page.place_order("Nagarajan", "India", "Bangalore", "8098800966", "08", "2030")

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
