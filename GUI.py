from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("https://img.alicdn.com/imgextra/i2/2743846318/O1CN01Z5VV3q1wXhHVll8hV_!!2743846318.jpg")

# Find the image element
image_element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.TAG_NAME, "img"))
)

# Right-click on the image element
action = webdriver.ActionChains(driver)
action.context_click(image_element).perform()

# Wait for the context menu to appear
time.sleep(1)

# Press the "V" key to select "Save Image As"
pyautogui.press('v')

# Wait for the save dialog to appear
time.sleep(1)

# Navigate to the directory input field
pyautogui.press('tab')  # press tab to focus on the directory input field
time.sleep(0.5)

# Enter the directory path and press Enter
pyautogui.typewrite('C:\\Users\\samco\\Desktop\\taobao scraper\\images\\')
pyautogui.press('enter')
time.sleep(0.5)

# Enter the file name and press Enter
pyautogui.typewrite('image.jpg')
pyautogui.press('enter')
time.sleep(5)