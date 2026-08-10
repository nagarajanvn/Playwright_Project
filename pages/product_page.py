from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.cart_page import CartPage


class ProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def add_to_cart(self) -> None:
        self.page.once("dialog", lambda dialog: dialog.dismiss())
        self.page.get_by_role("link", name="Add to cart").click()

    def open_cart(self) -> CartPage:
        self.page.get_by_role("link", name="Cart", exact=True).click()
        return CartPage(self.page)
