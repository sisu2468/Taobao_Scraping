from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# driver = webdriver.Chrome(options=options)

try:
    # Replace with your browser driver
    driver = webdriver.Chrome(options=options)

    # Navigate to the website
    driver.get("https://world.taobao.com/")


    # Find the search box element by its ID
    search_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "searchbar-input"))
    )
    button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "search-box"))
    )
    print(search_box.tag_name)
    

    # Input the text in the search box
    search_box.send_keys("men")
    button.click()
    print("wrote")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser window
    driver.quit()