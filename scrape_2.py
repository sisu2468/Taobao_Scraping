from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
import re
import pandas as pd
import tkinter as tk
from bs4 import BeautifulSoup
import requests
import time
import pyautogui


def my_python_function(url):
    # Your Python function implementation here
    print(f"URL submitted: {url}")


def submit_url():
    global url
    url = url_input.get()

    root.destroy()  # Close the GUI window


root = tk.Tk()
root.title("商品データ抽出ツール")

url_input_container = tk.Frame(root, bg="#f0f0f0")
url_input_container.pack(padx=20, pady=20)

tk.Label(url_input_container, text="商品URL", font=(
    "Helvetica", 16)).pack(side=tk.LEFT, padx=10)
url_input = tk.Entry(url_input_container, width=30, font=("Helvetica", 16))
url_input.pack(side=tk.LEFT, padx=10)

submit_btn = tk.Button(root, text="確認", command=submit_url,
                       bg="#4CAF50", fg="white", font=("Helvetica", 16))
submit_btn.pack(pady=20)

root.mainloop()

chrome_profile_path = r"C:\Users\samco\AppData\Local\Google\Chrome\User Data\Default"

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument('--profile-directory=Profile 3')
chrome_options.add_argument("--no-default-browser-check")

# Initialize ChromeDriver with options
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

driver.get(url)

time.sleep(5)
parsed_url = urlparse(url)
query_params = parse_qs(parsed_url.query)

id_value = query_params.get('id', [None])[0]

print(id_value)
# Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.url_to_be(url))
original_window = driver.current_window_handle

# Get the page source
page_source = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page_source, features="html.parser")

# Find the elements with the class "originPrice"
origin_price_element = soup.find(class_="Price--originPrice--2c8ipVx")
Origin_title = soup.find(class_="ItemTitle--mainTitle--2OrrwrD f-els-2")
Origin_parameters = soup.find_all(class_="InfoItem--infoItemContent--3ia0hBf")

# Find the div elements with class 'descV8-richtext'
div_elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'descV8-richtext'))
)

# Scroll to each div element containing images and download images
image_urls = []
image_count = 1

for div in div_elements:
    # Find all images within the div
    images = div.find_elements(By.TAG_NAME, 'img')

    for img in images:
        # Scroll the image into view
        driver.execute_script("arguments[0].scrollIntoView(true);", img)
        time.sleep(2)  # Give some time for the image to load

        # Wait for the image to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of(img)
        )

        # Get the image URL
        img_url = img.get_attribute('src')
        print(img_url)
        if not img_url.startswith(('http:', 'https:')):
            img_url = f"https:{img_url}"

        # Download the image and save it
        filename = f"image_{image_count}.jpg"
        original_url = driver.current_url

        # Open the image URL in a new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(img_url)

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
        pyautogui.typewrite(filename)
        pyautogui.press('enter')
        time.sleep(5)

        # Save the image URL
        image_urls.append(img_url)
        image_count += 1

        # Close the current tab and switch back to the original window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Ensure the original URL is loaded
        WebDriverWait(driver, 10).until(
            EC.url_contains(original_url)
        )
        time.sleep(10)

price = origin_price_element.text
product_name = Origin_title.text
size = Origin_parameters[0].text
color = Origin_parameters[1].text
print(image_urls)
images = []
imagess = soup.find_all('img', class_='descV6-mobile-image')
data = [{"商品名": product_name, "商品ID": id_value, "color": color,
         "size": size, "Product URL": url, "価格": price}]

# Extract the source of each image
for img in imagess:
    src = img.get('src')
    images.append(src)
    print(src)

print("product size", size)
print("product color", color)
print("product name", product_name)
print("price", price)


sizes = size.split(',')
items = color.split(',')

# Extract unique colors from items
colors = list(set(re.findall(r'粉色|紫色', color)))

# Create a list to hold the color-size combinations
combinations = []

# Iterate over each color and size combination
for colorr in colors:
    for sizze in sizes:
        # Append a row to the combinations for each combination
        combinations.append({'color': colorr, 'size': sizze})


# Step 3: Convert your data into a DataFrame
df = pd.DataFrame(data)
columns_to_add = ["カテゴリー", "メモ", "URL", "元", "原価", "関税10％、消費税8％、空輸代",
                  "原価合計", "売価", "修正売価", "純益", "純益2", "商品名2", "説明", "価格2",
                  "純益率", "10％OFF", "利益", "利益率", "在庫数", "公開状態", "表示順", "種類名", "種類在庫数"]

df = df.assign(**{col: "" for col in columns_to_add})

df_combined = pd.concat([df.assign(color=combo['color'], size=combo['size']) for combo in combinations], ignore_index=True)


for i, url in enumerate(image_urls):
    df[f'画像{i+1}'] = url

print(df_combined)


output_csv_file = 'output_combined.csv'
df_combined.to_csv(output_csv_file, index=False, encoding='utf-8-sig')

print("Data exported to output.csv")
driver.quit()


# df = pd.read_csv('output_combined.csv')
# df = df[['A', 'E', 'B', 'C', 'D']]  # Rearrange columns
# df.to_csv('output.csv', index=False)
