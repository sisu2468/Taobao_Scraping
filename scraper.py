from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to your WebDriver executable
webdriver_service = Service(r'C:\Users\samco\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')

# Set up the WebDriver (temporarily removing headless mode for debugging)
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Commented out headless mode
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=webdriver_service, options=options)

def scrape_mens_clothing():
    try:
        # Open Taobao
        driver.get("https://world.taobao.com/")
        
        # Wait for the search bar to be present
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "a2141.241046-hk.searchbar.i0.41ca5adbRkJcgW"))
        )
        logger.print("Found Search Bar")

        
        
        # Enter the search term for men's clothing
        search_box.send_keys("男装")  # Chinese characters for men's clothing
        search_box.send_keys(Keys.RETURN)
        
        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "item J_MouserOnverReq"))
        )
        
        # Scroll down to load more items
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "item J_MouserOnverReq"))
        )
        
        # Extract page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Scrape item names
        item_names = []
        items = soup.find_all("div", class_="item J_MouserOnverReq")
        for item in items:
            name_tag = item.find("a", class_="J_ClickStat")
            if name_tag:
                item_names.append(name_tag.get("title"))
        
        return item_names

    except Exception as e:
        logger.error("An error occurred during scraping:", exc_info=True)
        # Log the page source for debugging
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        return []

    finally:
        driver.quit()

# Scrape men's clothing item names
mens_clothing_items = scrape_mens_clothing()
print("Men's Clothing Items:")
for item in mens_clothing_items:
    print(item)
