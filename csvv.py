from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Initialize a web driver instance to control a Chrome window
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Visit the target page
driver.get('https://finance.yahoo.com/quote/MSFT/history/')

time.sleep(5)

# Wait for the date picker to be clickable
date_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tertiary-btn"))
        )
print("Found Date Bar")
date_box.click()

dateinput = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "svelte-grkcsd"))
        )




first_data=dateinput[4]
second_date=dateinput[6]



# Clear the date picker input field
first_data.clear()
second_date.clear()

# Enter the start date
first_data.send_keys('01-01-2000')

# Enter the end date
second_date.send_keys('04-06-2024')

done_Button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "primary-btn"))
        )

done_Button.click()

time.sleep(5)

download_button = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "fin-size-medium"))
        )

download_button[0].click()
time.sleep(5)

# Close the browser and free up the resources
driver.quit()