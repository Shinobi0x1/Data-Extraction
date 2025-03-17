import time
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def main():

    # Set up Web driver
    driver = webdriver.Firefox()

    # grab the website
    monster_data = []
    for page in range(1, 6):
        driver.get(f"https://www.popmart.com/us/collection/1?page={page}&sortWay=1&brandIDs=15&collectionId=1")

        # Let us try to determine what is the best time rate for the page to render completely then change to the next page using time.sleep()
        time.sleep(12)

        products_container = driver.find_elements(By.CSS_SELECTOR, "div.index_productItemContainer__rDwtr.false")

        for container in products_container:
            try:
                # Extract the image, name, and price
                items_image = container.find_element(By.CSS_SELECTOR, "img.ant-image-img").get_attribute("src")
                items_name = container.find_element(By.CSS_SELECTOR, "h2.index_itemUsTitle__7oLxa").text.strip()
                items_price = container.find_element(By.CSS_SELECTOR, "div.index_itemPrice__AQoMy").text.strip()

                monster_data.append({
                    'Item Name': items_name,
                    'Item Price': items_price,
                    'Image Url': items_image,
                })
            except NoSuchElementException:
                print("Some product details are missing, skipping this item..")


        try:
            # Accept the policy if pop's up
            accept = driver.find_element(By.CSS_SELECTOR, "div.policy_acceptBtn__ZNU71")
            ActionChains(driver).move_to_element(accept).click().perform()
        except NoSuchElementException:
             pass
        except TimeoutError:
            print("Accept button not clickable or pop-up not present..")
    df = pd.DataFrame(monster_data)
    df.to_excel("monster.xlsx", index=False)


main()