
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By

# service = Service("/usr/local/bin/chromedriver")

# driver = webdriver.Chrome(service=service)

# driver.get("https://www.google.com")
# print(driver.title)
# driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class OpenCartAutomation:
    def __init__(self):
        # Specify the exact path to chromedriver
        self.driver_path = "/usr/local/bin/chromedriver"
        
        # Initialize the Chrome driver with the specified path
        self.service = Service(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=self.service)

    def navigate_to_website(self):
        # Navigate to the website
        self.driver.get("https://demo.opencart.com/")
        time.sleep(5)

    def search_for_product(self, product_name):
        time.sleep(3)
        # Search for the product
        search_box = self.driver.find_element(By.NAME, "search")
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results page to load
        time.sleep(5)

    def open_product_page(self):
        # Click on the first product to open its details page using JavaScript
        product_link = self.driver.find_element(By.CLASS_NAME, "product-thumb").find_element(By.TAG_NAME, "a")
        self.driver.execute_script("arguments[0].click();", product_link)

        # Wait for the product page to load
        time.sleep(5)

    def add_to_cart(self):
        # Add the product to the cart using JavaScript to avoid interception issues
        add_to_cart_button = self.driver.find_element(By.ID, "button-cart")
        self.driver.execute_script("arguments[0].click();", add_to_cart_button)

        # Wait for the cart to update and retrieve the cart quantity
        try:
            # Explicit wait for the cart total to be visible and updated
            cart_total_element = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.ID, "cart-total"))
            )
            print(f"Cart Quantity: {cart_total_element.text.split()[0]}")  # Print only the quantity
        except Exception as e:
            print(f"Could not retrieve cart quantity: {e}")

    def close_browser(self):
        # Close the browser
        self.driver.quit()

def main():
    automation = OpenCartAutomation()
    automation.navigate_to_website()
    automation.search_for_product("MacBook")
    automation.open_product_page()
    automation.add_to_cart()  # Product added to the cart here
    automation.close_browser()

if __name__ == "__main__":
    main()


