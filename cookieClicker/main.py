from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_webdriver_path = "Path to your chrome web driver here"
ser = Service(chrome_webdriver_path)
driver = webdriver.Chrome(service=ser)
driver.get("https://orteil.dashnet.org/cookieclicker/")

start_time = time.time()
initial_time = time.time()
cookie = driver.find_element(By.ID, "bigCookie")

game_on = True

while game_on:
    cookie.click()

    # after 5 seconds

    if time.time() - initial_time > 5:

        # getting variables and formatting them

        cookies = driver.find_element(By.ID, "cookies")
        cookies = str(cookies.text).replace(",", "")
        prices = driver.find_elements(By.CSS_SELECTOR, ".content .price")
        formatted_prices = [price.text for price in prices if price.text != ""]
        for price in formatted_prices:
            if "," in price:
                new_price = str(price).replace(",", "")
                index = formatted_prices.index(price)
                formatted_prices[index] = new_price

        formatted_prices = [int(price) for price in formatted_prices]

        # check if the max price is affordable

        for price in formatted_prices:
            max_price = max(formatted_prices)
            max_price_index = formatted_prices.index(max_price)
            if max_price > int(cookies.split(" ")[0]):
                formatted_prices[max_price_index] = 0

        if max_price_index is not None:
            clickable_id = f"product{max_price_index}"
            driver.find_element(By.ID, clickable_id).click()

        initial_time = time.time()

    # after 5 minutes stop the game

    if time.time() - start_time > 1*60:
        game_on = False
        print(driver.find_element(By.ID, "cookies"))
        driver.close()
