from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
service = Service(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("https://google.com")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "gLFyf")))
input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
input_element.clear()
input_element.send_keys("youtube" + Keys.ENTER)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "gLFyf")))
link = driver.find_element(By.PARTIAL_LINK_TEXT, "YouTube")
link.click()
print("Page title is:", driver.title)
time.sleep(5)
driver.quit()
