from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# driver = webdriver.Chrome(options=options)

try:
    # Replace with your browser driver
    driver = webdriver.Chrome(options=options)

    # Navigate to the website
    driver.get("https://world.taobao.com/")

    print("LOGIN.......")
    # Find the search box element by its ID
    # search_box = WebDriverWait(driver, 5).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "searchbar-input"))
    # )
    # button = WebDriverWait(driver, 5).until(
    #     EC.presence_of_element_located((By.ID, "search-box"))
    # )
    # print(search_box.tag_name)
    

    # Input the text in the search box
    # search_box.send_keys("men")
    # button.click()
    print("starting....")
    titles = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "promo-icon-wrap"))
    )

    promo_divs=driver.find_elements(By.CLASS_NAME, "promo-icon-wrap")

    promo_texts = []
    for div in promo_divs:
        span = div.find_element(By.TAG_NAME, "span")
        if span:
            promo_texts.append(span.text)
        
    print(promo_texts)

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser window
    driver.quit()