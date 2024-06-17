from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import csv
import time

# Set up the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
url = "https://item.taobao.com/item.htm?id=754835047515&ali_trackid=2:mm_26632943_457000242_108857250342:1718433646_046_315558778&rid=2852359894&spm=a21412.affiliate.promote.2852359894&union_lens=lensId:OPT@1718433641@21508ab6_0de8_1901aa075c6_305e@01@eyJmbG9vcklkIjo2OTE5OH0ie;recoveryid:046_998718587@1718433646991&relationId=2852359894&bxsign=tbkUGJpC3i7qVNdAikgS5nIIlASg-vKw8Si171WZ70J9MtQOWJ-cbOlphFRWbcuF1pSHm5qi8pePVeP-9saQ_EQIIT0c4gwKQCz6g4jyeQi8-mEPJtzO0InJw2g5oGlyxRTtFG4avsmxnvecAiCp_WDfOwxTo0xGGVUsX8xRbK8NRfydeOef1_NVxyXUNexPkHt&skuId=5259956309620"
driver.get(url)

time.sleep(50)
parsed_url = urlparse(url)
query_params = parse_qs(parsed_url.query)

id_value = query_params.get('id', [None])[0]

print(id_value)
# Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.url_to_be(url))

# Get the page source
page_source = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page_source, features="html.parser")

# Find the elements with the class "originPrice"
origin_price_element = soup.find(class_="Price--originPrice--2c8ipVx")
Origin_title = soup.find(class_="ItemHeader--mainTitle--1rJcXZz f-els-2")
Origin_parameters = soup.find_all(class_="InfoItem--infoItemContent--3ia0hBf")

price = origin_price_element.text
product_name = Origin_title.text
# price = origin_price_element.find(class_="Price--priceText--1oEHppn").text
size = Origin_parameters[0].text
color = Origin_parameters[1].text
images =[]
imagess = soup.find_all('img', class_='descV6-mobile-image')
data = [{"商品名": product_name, "商品ID": id_value, "color": color, "size": size, "価格": price, "images": ",".join(images)}]

# Extract the source of each image
for img in imagess:
    src = img.get('src')
    images.append(src)
    print(src)

print("product size", size)
print("product color", color)
print("product name", product_name)
print("price", price)

# Step 3: Convert your data into a DataFrame
df = pd.DataFrame(data)

# Step 4: Export the DataFrame to a CSV file
df.to_csv('output.csv', index=False)

print("Data exported to output.csv")
# with open("output.csv", "w", newline="") as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=["product_name", "product_id", "color", "size", "price", "images"])
#     writer.writeheader()
#     writer.writerows(data)
driver.quit()