from selenium.webdriver.common.by import By
from page_objects.barbora_product import BarboraProduct


class BarboraScraper:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.hrefs = []
        self.categories = []

    def scrape_data(self):
        self.accept_cookies()
        self.age_consent()
        self.get_all_categories()
        # self.get_urls()
        # self.get_product_data()

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
        category_elements = self.driver.find_elements(By.CSS_SELECTOR, ".desktop-menu--parent-category-list .category-item--title")
        broad_category_links = [link.get_attribute('href') for link in category_elements]
        [print(link) for link in broad_category_links]
        narrow_category_links = []
        for broad_category_link in broad_category_links:
            self.driver.get(broad_category_link)
            narrow_category_elements = self.driver.find_elements(By.CSS_SELECTOR, ".category-tree--grand-child-category-list .category-item--title")
            narrow_links = [el.get_attribute('href') for el in narrow_category_elements]
            narrow_category_links.extend(narrow_links)
        [print(link) for link in narrow_category_links]
        self.categories = narrow_category_links


    def get_urls(self):
        for i in range(1, 100):
            self.driver.get(f"{self.url}?page={i}")
            cards = self.driver.find_elements(By.CSS_SELECTOR, ".tw-flex-shrink-0.tw-list-none.tw-w-full")
            print(f"rasta korteliu {len(cards)}")
            for card in cards:
                href = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
                self.hrefs.append(href)
            if len(cards) == 0:
                break

    def get_product_data(self):
        # self.hrefs = ["https://barbora.lt/produktai/grikiu-kruopos-skaneja-4-x-125-g-500-g"]
        [print(link) for link in self.hrefs]
        for link in self.hrefs:
            self.driver.get(link)
            product = BarboraProduct(self.driver)
            product.fill()
            product.save_category()
            product.save()

