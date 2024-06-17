from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse, parse_qs
import time
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


driver = webdriver.Chrome(options=options)
    

    # Navigate to the website
url = "https://item.taobao.com/item.htm?id=754835047515&ali_trackid=2:mm_26632943_457000242_108857250342:1718433646_046_315558778&rid=2852359894&spm=a21412.affiliate.promote.2852359894&union_lens=lensId:OPT@1718433641@21508ab6_0de8_1901aa075c6_305e@01@eyJmbG9vcklkIjo2OTE5OH0ie;recoveryid:046_998718587@1718433646991&relationId=2852359894&bxsign=tbkUGJpC3i7qVNdAikgS5nIIlASg-vKw8Si171WZ70J9MtQOWJ-cbOlphFRWbcuF1pSHm5qi8pePVeP-9saQ_EQIIT0c4gwKQCz6g4jyeQi8-mEPJtzO0InJw2g5oGlyxRTtFG4avsmxnvecAiCp_WDfOwxTo0xGGVUsX8xRbK8NRfydeOef1_NVxyXUNexPkHt&skuId=5259956309620"
driver.get(url)    

print("LOGIN.......")
time.sleep(60)
parsed_url = urlparse(url)
query_params = parse_qs(parsed_url.query)

id_value = query_params.get('id', [None])[0]

print(id_value)



Pric = driver.find_element(By.CLASS_NAME, "originPrice")

# product_nam = driver.find_element(By.CLASS_NAME, "ItemHeader--mainTitle--1rJcXZz f-els-2")
# print(search_box.tag_name)
# product_price=Pric.text
# product_name=product_nam.text

# print("product name", product_name)
print(Pric)

# Input the text in the search box
# search_box.send_keys("男装")
# button.click()

# promo_links = driver.find_elements(By.CLASS_NAME, "Card--doubleCardWrapper--L2XFE73")
# product_names = []
# prices=[]
# original_window = driver.window_handles[0]

# stop_scraping = False


# for promo_link in promo_links:
#     if stop_scraping:
#         print("breaking")
#         break
#     # Click on the promo link to open a new window
#     promo_link.click()
#     # Wait for the new window to load
#     WebDriverWait(driver, 10).until(EC.new_window_is_opened)
    
#       # Switch to the new window
#     new_window = [window for window in driver.window_handles if window != original_window][0]
#     driver.switch_to.window(new_window)
#     print("waiting for the new window to load......")
#     time.sleep(40)
#     # Scrape the product name
#     print()
#     product_name = driver.find_element(By.CLASS_NAME, "ItemHeader--mainTitle--1rJcXZz")
#     image_url = driver.find_elements(By.CLASS_NAME, "PicGallery--thumbnailPic--1spSzep")
#     price = driver.find_element(By.CLASS_NAME, "Price--priceText--1oEHppn")
    
#     # product_number = driver.find_element(By.ID, "pc_detail.29232929/evo401271b517998.202205.i1.56c67dd6WaKSRs")
    

#     # image1 = image_url[0].get_attribute("src")
#     # image2 = image_url[1].get_attribute("src")
#     # image3 = image_url[2].get_attribute("src")
#     # image4 = image_url[3].get_attribute("src")
#     # image5 = image_url[4].get_attribute("src")
#     # print("image 1 uri: ", image1)
#     product_names.append(product_name.text)
#     prices.append(price.text)
#     print(image_url)
#     # product_names.append(product_name)
#     print(product_names)
#     print(prices)
#     # print("product id: ", product_id)
#     # Switch back to the original window
    
#      # Close the new window
#     driver.close()
    
#     # Switch back to the original window
#     driver.switch_to.window(original_window)
#     n=input("want to quit??")
#     if n=="yes":
#         stop_scraping=True
#     else:
#         continue

# data = {
#     "PRODUCT NAME": product_names,
#     "PRICE": prices
# }
# df = pd.DataFrame(data)

# # Save the DataFrame to a CSV file
# csv_file_path = 'products.csv'
# df.to_csv(csv_file_path, index=False)

# print(f"Data successfully saved to {csv_file_path}")