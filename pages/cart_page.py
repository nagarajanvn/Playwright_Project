from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def place_order(
        self,
        name: str,
        country: str,
        city: str,
        credit_card: str,
        month: str,
        year: str,
    ) -> None:
        self.page.goto("https://www.demoblaze.com/cart.html")
        self.page.get_by_role("button", name="Place Order").click()
        self.page.get_by_role("textbox", name="Total: 1100 Name:").fill(name)
        self.page.get_by_role("textbox", name="Total: 1100 Name:").press("Tab")
        self.page.get_by_role("textbox", name="Country:").fill(country)
        self.page.get_by_role("textbox", name="Country:").press("Tab")
        self.page.get_by_role("textbox", name="City:").fill(city)
        self.page.get_by_role("textbox", name="City:").press("Tab")
        self.page.get_by_role("textbox", name="Credit card:").fill(credit_card)
        self.page.get_by_role("textbox", name="Credit card:").press("Tab")
        self.page.get_by_role("textbox", name="Month:").fill(month)
        self.page.get_by_role("textbox", name="Month:").press("Tab")
        self.page.get_by_role("textbox", name="Year:").fill(year)
        self.page.get_by_role("textbox", name="Year:").press("Tab")
        self.page.get_by_role("button", name="Purchase").click()
        self.page.get_by_role("button", name="OK").click()
