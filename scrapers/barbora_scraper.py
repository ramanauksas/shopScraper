from selenium.webdriver.common.by import By
from page_objects.barbora_product import BarboraProduct
from datetime import datetime
import time

from page_objects.db import DB


class BarboraScraper:
    def __init__(self, driver, url):
        self.driver = driver
        self.db = None
        self.url = url
        self.hrefs = []
        self.categories = []


    def scrape_data(self):
        self.accept_cookies()
        self.age_consent()
        # self.get_all_categories()
        # self.get_urls()
        self.get_product_data()

    def accept_cookies(self):
        self.driver.get(self.url)
        cookie_button = self.driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll')
        cookie_button.click()

    def age_consent(self):
        self.driver.get(self.url)
        is_20 = len(self.driver.find_elements(By.ID, 'fti-modal-option-1')) != 0
        if is_20:
            age_consent_button = self.driver.find_element(By.ID, "fti-modal-option-1")
            age_consent_button.click()

    def get_all_categories(self):
        self.db = DB()
        category1_elements = self.driver.find_elements(By.CSS_SELECTOR, ".desktop-menu--parent-category-list .category-item--title")
        category1_text_list = [el.find_element(By.CSS_SELECTOR, 'a span').text for el in category1_elements]
        category1_href_list = [el.get_attribute('href') for el in category1_elements]
        category1_dict = {text: href for text, href in zip(category1_text_list, category1_href_list)}

        for category1 in category1_dict.keys():
            print(category1)
            self.driver.get(category1_dict[category1])
            category23_elements = self.driver.find_elements(By.CLASS_NAME, "category-tree--child-category")
            for category23_element in category23_elements:
                list_items = category23_element.find_elements(By.CSS_SELECTOR, 'a.category-item--title')
                if len(list_items) > 0:
                    category2 = list_items[0].find_element(By.TAG_NAME, 'span').text
                    print(category2)
                    for item in list_items:
                        category3 = item.find_element(By.TAG_NAME, 'span').text
                        link = item.get_attribute('href')
                        print(link)
                        category = [category1, category2, category3, link, 1]
                        print(category)
                        self.save_category(category)
        self.db.close()

    def save_category(self, category):
        # Check if the category exists, if not, insert it and get its ID
        query = "SELECT id FROM `categories` WHERE `category1` = %s AND `category2` = %s AND `category3`= %s AND `link`=%s AND `store`= %s"
        cursor = self.db.conn.cursor()
        cursor.execute(query, (*category,))
        result = cursor.fetchone()

        if not result:
            # Category does not exist, insert it
            query = "INSERT INTO `categories` (`category1`, `category2`, `category3`, `link`, `store`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (*category,))
            self.db.conn.commit()
            # Get the newly inserted category ID
            # self.category = cursor.lastrowid


    def get_urls(self):
        self.db = DB()
        query = "SELECT id, link FROM `categories` WHERE `store`= %s"
        cursor = self.db.conn.cursor()
        cursor.execute(query, (1,))
        categories = cursor.fetchall()

        for index, category in enumerate(categories):
            category_id = category[0]
            category_url = category[1]

            print(f"{index+1}/{len(categories)} - {category_url}")
            for i in range(1, 1000):
                self.driver.get(f"{category_url}?page={i}")
                cards = self.driver.find_elements(By.CSS_SELECTOR, ".tw-flex-shrink-0.tw-list-none.tw-w-full")
                print(f"rasta korteliu {len(cards)}")
                for card in cards:
                    product_url = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    # self.hrefs.append(href)
                    self.save_url(product_url, category_id)
                if len(cards) == 0:
                    break
        self.db.close()

    def save_url(self, product_url, category_id):
        # Check if the category exists, if not, insert it and get its ID
        query = "SELECT id FROM `urls` WHERE `url` = %s AND `category` = %s"
        cursor = self.db.conn.cursor()
        cursor.execute(query, (product_url, category_id))
        result = cursor.fetchone()

        if not result:
            # If product url does not exist, insert it
            updated_at = datetime.now()
            query = "INSERT INTO `urls` (`url`, `category`, `updated_at`) VALUES (%s, %s, %s)"
            cursor.execute(query, (product_url, category_id, updated_at))
            self.db.conn.commit()
            # Get the newly inserted category ID
            # self.category = cursor.lastrowid


    def get_product_data(self):
        # self.hrefs = ["https://barbora.lt/produktai/grikiu-kruopos-skaneja-4-x-125-g-500-g"]
        self.db = DB()
        query = "SELECT id, url FROM `urls`"
        cursor = self.db.conn.cursor()
        cursor.execute(query)
        all_url_tuples = cursor.fetchall()

        query = "SELECT link FROM `product`"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        existing_product_links = [link[0] for link in results]

        url_tuples = [url_tuple for url_tuple in all_url_tuples if url_tuple[0] not in set(existing_product_links)]

        # [print(link) for link in self.hrefs]
        for url_tuple in url_tuples:
            url_id, url = url_tuple
            self.driver.get(url)
            print(url)
            barbora_product = BarboraProduct(self.driver)
            barbora_product.fill(url_id)
            if barbora_product.title and barbora_product.unit and barbora_product.category:
                barbora_product.save()

        time.sleep(1000)

