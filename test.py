from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time

# --------- Base Test Class (Encapsulation & Concatenation) ---------
class BaseTest:
    def __init__(self, base_url):
        # encapsulated driver
        self.__driver = webdriver.Chrome()
        self.base_url = base_url

    def open(self, path=""):
        """https://www.flipkart.com/"""
        full_url = self.base_url + path
        self.__driver.get(full_url)
        self.__driver.maximize_window()

    def close(self):
        """Gracefully quit driver."""
        time.sleep(1)
        self.__driver.quit()

    def driver(self):
        """Expose driver to subclasses."""
        return self.__driver

# --------- Test Interface (Polymorphism) ---------
class TestCaseInterface:
    def run(self):
        raise NotImplementedError("Must implement run()")

# --------- Login Test ---------
class LoginTest(BaseTest, TestCaseInterface):
    def __init__(self, base_url, username, password):
        super().__init__(base_url)
        self.username = username
        self.password = password

    def run(self):
        self.open("/login")
        d = self.driver()
        d.find_element(By.ID, "username").send_keys(self.username)
        d.find_element(By.ID, "password").send_keys(self.password)
        d.find_element(By.ID, "loginBtn").click()
        time.sleep(2)
        assert d.find_element(By.ID, "logoutBtn").is_displayed(), "Login failed!"
        print("✅ LoginTest passed")
        self.close()

# --------- Product Search Test ---------
class SearchTest(BaseTest, TestCaseInterface):
    def __init__(self, base_url, query):
        super().__init__(base_url)
        self.query = query

    def run(self):
        self.open("/")
        d = self.driver()
        d.find_element(By.NAME, "search").send_keys(self.query)
        d.find_element(By.CSS_SELECTOR, "button.search-btn").click()
        time.sleep(2)
        results = d.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(results) > 0, "No products found!"
        print(f"✅ SearchTest passed: found {len(results)} items for '{self.query}'")
        self.close()

# --------- Add to Cart Test ---------
class AddToCartTest(BaseTest, TestCaseInterface):
    def __init__(self, base_url, product_id):
        super().__init__(base_url)
        self.product_id = product_id

    def run(self):
        self.open(f"/product/{self.product_id}")
        d = self.driver()
        d.find_element(By.ID, "addToCartBtn").click()
        time.sleep(1)
        cart_count = d.find_element(By.ID, "cart-count").text
        assert int(cart_count) >= 1, "Add to cart failed!"
        print("✅ AddToCartTest passed")
        self.close()

# --------- Test Runner ---------
if __name__ == "__main__":
    BASE_URL = "https://yourshop.com"

    tests = [
        LoginTest(BASE_URL, "testuser@example.com", "S3cr3tPass!"),
        SearchTest(BASE_URL, "wireless headphones"),
        AddToCartTest(BASE_URL, "12345")
    ]

    for test in tests:
        try:
            test.run()
        except AssertionError as e:
            print(f"❌ {test.__class__.__name__} failed: {e}")
