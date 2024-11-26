from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page_objects.rimi_product import RimiProduct
import time



class RimiScraper:
    def __init__(self, driver, wait, url):
        self.driver = driver
        self.wait = wait
        self.url = url
        self.hrefs = []

    def scrape_data(self):
        self.accept_cookies()
        self.close_modal()
        self.close_modal()
        self.close_language_options()
        self.get_urls()
        self.get_product_data()

        # time.sleep(1000)

    def accept_cookies(self):
        self.driver.get(self.url)
        cookie_button = self.driver.find_element(By.ID, 'CybotCookiebotDialogBodyButtonDecline')
        cookie_button.click()

    def close_modal(self):
        self.driver.get(self.url)
        try:
            modal_close_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.modal__close')))
            modal_close_button.click()
        except:
            pass

    def close_language_options(self):
        language_buttons = self.driver.find_elements(By.CSS_SELECTOR, '.gtm')
        if len(language_buttons)>0:
            language_buttons[0].click()

    def get_urls(self):
        for i in range(1, 100):
            self.driver.get(f"{self.url}?currentPage={i}")
            cards = self.driver.find_elements(By.CSS_SELECTOR, ".product-grid__item")
            print(f"rasta korteliu {len(cards)}")
            for card in cards:
                href = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
                self.hrefs.append(href)
            if len(cards) == 0:
                break

    def get_product_data(self):
        # self.hrefs = ["https://www.rimi.lt/e-parduotuve/lt/produktai/alkoholiniai-ir-nealkoholiniai-gerimai/alus/sviesus-alus/nefiltr-svies-kanapinis-alus-5-1-1-l/p/1359333"]
        [print(link) for link in self.hrefs]
        for link in self.hrefs:
            self.driver.get(link)
            product = RimiProduct(self.driver)
            product.fill()
            if bool(product.price):
                product.save_category()
                product.save()

