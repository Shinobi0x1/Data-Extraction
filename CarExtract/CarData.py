"""
    March 18, 2025

    Today we will learn how to go back from let say a page that has data then back to
    the list of cars.


"""
import pandas as pd
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def main():
    # Set up WebDriver
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0")
    driver = webdriver.Firefox(options=options)

    # Open Craigslist page
    driver.get("https://losangeles.craigslist.org/search/sfv/cta#search=2~gallery~0")
    time.sleep(5)

    car_data = []
    # Extract all the href links from the listings
    listing_elements = driver.find_elements(By.CSS_SELECTOR, '.cl-search-result a')
    links = list({elem.get_attribute('href') for elem in listing_elements if elem.get_attribute('href')})

    for link in links:
        driver.get(link)
        title = driver.find_element(By.CLASS_NAME, 'postingtitle').text
        try:
            vehicleYear = driver.find_element(By.CLASS_NAME, 'attr.important').text
        except NoSuchElementException:
            vehicleYear = 'n/a'
        try:
            fuelType = driver.find_element(By.CLASS_NAME, 'attr.auto_fuel_type').text
        except NoSuchElementException:
            fuelType = 'n/a'
        try:
            odometer = driver.find_element(By.CLASS_NAME, 'attr.auto_title_status').text
        except NoSuchElementException:
            odometer = 'n/a'
        try:
            transmission = driver.find_element(By.CLASS_NAME, 'attr.auto_transmission').text
        except NoSuchElementException:
            transmission = 'n/a'
        try:
            body_type = driver.find_element(By.CLASS_NAME, 'attr.auto_bodytype').text
        except NoSuchElementException:
            body_type = 'n/a'


        car_data.append(
            {
                'Title': title,
                'Vehicle year': vehicleYear,
                'Fuel type': fuelType.split(':')[-1].strip(),
                'Odometer': odometer.split(':')[-1].strip(),
                'Transmission': transmission.split(':')[-1].strip(),
                'Body Type': body_type.split(':')[-1].strip(),
            }
        )

        time.sleep(5)
        driver.back()
        time.sleep(5)
        columns_order = ['Title', 'Vehicle year', 'Fuel type', 'Odometer', 'Transmission', 'Body Type']
        df = pd.DataFrame(car_data, columns=columns_order)
        df.to_excel("craigslist.xlsx", index=False)
main()
