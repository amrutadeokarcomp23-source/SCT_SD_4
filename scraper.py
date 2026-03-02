from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import re

def scrape_amazon(search_query):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://www.amazon.in/s?k={search_query}"
    driver.get(url)
    time.sleep(4)

    products = []

    items = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

    for item in items:
        try:
            name = item.find_element(By.TAG_NAME, "h2").text
        except:
            continue

        try:
            price = item.find_element(By.CLASS_NAME, "a-price-whole").text
            price = price.replace(",", "")
            price = int(price)
        except:
            continue

        try:
           rating_element = item.find_element(By.XPATH, ".//span[@class='a-icon-alt']")
           rating_text = rating_element.get_attribute("innerHTML")
           rating = float(rating_text.split(" ")[0])
        except:
           rating = None


        products.append({
            "Name": name,
            "Price": price,
            "Rating": rating
        })

    driver.quit()

    # 🔥 Sort by price ascending
    products = sorted(products, key=lambda x: x["Price"])

    # 🔥 Get top 10 lowest priced products
    return products[:10]

