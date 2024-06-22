from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
import pandas as pd
import tkinter as tk
from bs4 import BeautifulSoup
import requests
import time

def my_python_function(url):
    # Your Python function implementation here
    print(f"URL submitted: {url}")

def submit_url():
    global url
    url = url_input.get()
    
    root.destroy()  # Close the GUI window

root = tk.Tk()
root.title("URL Input GUI")

url_input_container = tk.Frame(root, bg="#f0f0f0")
url_input_container.pack(padx=20, pady=20)

tk.Label(url_input_container, text="Write URL HERE", font=("Helvetica", 16)).pack(side=tk.LEFT, padx=10)
url_input = tk.Entry(url_input_container, width=30, font=("Helvetica", 16))
url_input.pack(side=tk.LEFT, padx=10)

submit_btn = tk.Button(root, text="Go", command=submit_url, bg="#4CAF50", fg="white", font=("Helvetica", 16))
submit_btn.pack(pady=20)

root.mainloop()

chrome_profile_path = r"C:\Users\samco\AppData\Local\Google\Chrome\User Data\Default"

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument('--profile-directory=Profile 1')
chrome_options.add_argument("--no-default-browser-check")

# Initialize ChromeDriver with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(url)

time.sleep(15)
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

div_elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'descV8-richtext'))
)

print(div_elements)

# Scroll to each div element containing images and download images
image_urls = []
image_count = 1
for div in div_elements:
    # Scroll the div element into view
    driver.execute_script("arguments[0].scrollIntoView(true);", div)
    time.sleep(2)  # Give some time for images to load

    # Find all images within the div
    images = div.find_elements(By.TAG_NAME, 'img')

    for img in images:
        # Wait for the image to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of(img)
        )

        # Get the image URL
        img_url = img.get_attribute('src')
        if not img_url.startswith(('http:', 'https:')):
            img_url = f"https:{img_url}"

        # Download the image and save it
        filename = f"image_{image_count}.jpg"
        with open(filename, 'wb') as f:
            f.write(requests.get(img_url).content)
        print(f"Image saved: {filename}")

        # Save the image URL
        image_urls.append(img_url)
        image_count += 1

price = origin_price_element.text
product_name = Origin_title.text
size = Origin_parameters[0].text
color = Origin_parameters[1].text
images = []
imagess = soup.find_all('img', class_='descV6-mobile-image')
data = [{"商品名": product_name, "商品ID": id_value, "color": color, "size": size, "価格": price, "images": ",".join(image_urls)}]

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
driver.quit()
