from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


driver = webdriver.Chrome(options=options)
    

    # Navigate to the website
driver.get("https://pvp.giustizia.it/pvp/en/risultati_ricerca.page?ordinamento=data_vendita_decre&anno=&disponibilita=&lng=&categoria=immobile_residenziale&indirizzo=&elementiPerPagina=10&ricerca_libera=&ordine_localita=a_z&idInserzione=&tipo_bene=immobili&geo=raggio&view=tab&prezzo_da=&procedura=&raggio=25&prezzo_a=&lat=&tribunale")    


time.sleep(10)
# Find the search box element by its ID
search_box = WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "font-blue font18"))
)
print("Found Prices")
prices=[]


for price in search_box:
    prices.append(price.text)
    
print(prices)
# data = {
#     "PRODUCT NAME": product_names,
#     "PRICE": prices
# }
# df = pd.DataFrame(data)

# # Save the DataFrame to a CSV file
# csv_file_path = 'products.csv'
# df.to_csv(csv_file_path, index=False)

# print(f"Data successfully saved to {csv_file_path}")