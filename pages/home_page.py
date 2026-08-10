from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.product_page import ProductPage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def open(self) -> None:
        super().open("https://www.demoblaze.com/index.html")

    def login(self, username: str, password: str) -> None:
        self.page.get_by_role("link", name="Log in").click()
        self.page.locator("#loginusername").click()
        self.page.locator("#loginusername").fill(username)
        self.page.locator("#loginusername").press("Tab")
        self.page.locator("#loginpassword").fill(password)
        self.page.get_by_role("button", name="Log in").click()

    def open_product(self, product_name: str) -> ProductPage:
        self.page.locator("#next2").click()
        self.page.get_by_role("link", name=product_name).click()
        return ProductPage(self.page)
