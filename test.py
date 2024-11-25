from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AmazonAutomation:
    def __init__(self, chromedriver_path):
        self.service = Service(chromedriver_path)
        self.driver = None
        self.wait = None
    
    def setup_driver(self):
        """Initialize the Chrome WebDriver with some optimal settings"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)  # Increased timeout for better reliability
        
    def find_and_click_element(self, by, value, timeout=20):
        """Utility method to find and click elements with proper waiting"""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except TimeoutException:
            logging.error(f"Timeout waiting for element: {value}")
            return False

    def search_product(self, search_term):
        """Search for a product on Amazon"""
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
            )
            search_box.clear()
            search_box.send_keys(search_term)
            search_box.submit()
            logging.info(f"Searched for: {search_term}")
            return True
        except TimeoutException:
            logging.error("Could not find search box")
            return False

    def find_product_in_results(self, product_name):
        """Find a specific product in search results"""
        try:
            # Wait for search results to load
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component-type='s-search-result']"))
            )
            
            # Using a more reliable XPath to find products
            products = self.driver.find_elements(
                By.XPATH, 
                "//div[@data-component-type='s-search-result']//h2//a"
            )
            
            for product in products:
                title = product.get_attribute("aria-label") or product.text
                if product_name.lower() in title.lower():
                    logging.info(f"Found product: {title}")
                    return product.get_attribute("href")
            
            logging.warning("Product not found in search results")
            return None
            
        except Exception as e:
            logging.error(f"Error finding product: {str(e)}")
            return None

    def add_to_cart(self, product_url):
        """Navigate to product page and add to cart"""
        try:
            self.driver.get(product_url)
            return self.find_and_click_element(By.ID, "add-to-cart-button")
        except Exception as e:
            logging.error(f"Error adding to cart: {str(e)}")
            return False

    def view_cart(self):
        """View cart and return items"""
        try:
            self.find_and_click_element(By.ID, "nav-cart")
            cart_items = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sc-product-title"))
            )
            return [item.text.strip() for item in cart_items]
        except Exception as e:
            logging.error(f"Error viewing cart: {str(e)}")
            return []

    def run_automation(self, search_term, product_name):
        """Main method to run the automation"""
        try:
            self.setup_driver()
            self.driver.get("https://www.amazon.in/")
            
            if not self.search_product(search_term):
                raise Exception("Failed to search for product")
            
            product_url = self.find_product_in_results(product_name)
            if not product_url:
                raise Exception("Product not found")
            
            if not self.add_to_cart(product_url):
                raise Exception("Failed to add product to cart")
            
            cart_items = self.view_cart()
            logging.info("Items in cart:")
            for item in cart_items:
                logging.info(f"- {item}")
                
            return True
            
        except Exception as e:
            logging.error(f"Automation failed: {str(e)}")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    # Example usage
    automation = AmazonAutomation("/usr/local/bin/chromedriver")
    automation.run_automation(
        search_term="iPhone 16",
        product_name="Apple iPhone 16 (128 GB) - Ultramarine"
    )
