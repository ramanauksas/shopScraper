from selenium.webdriver.common.by import By
from page_objects.product import Product


class RimiProduct(Product):
    def __init__(self, driver):
        super().__init__(driver)

    def fill(self):
        print("run fill method for rimi product")
        title_text_full = self.driver.find_element(By.TAG_NAME, "h1").text
        print(title_text_full)
        title_parts = title_text_full.split(",")

        # title
        self.title = title_parts[0]

        # property
        if len(title_parts)>2:
            self.property = ",".join(title_parts[1:-1])

        # size
        self.size = title_parts[-1].split()[0]
        li_element = self.driver.find_element(By.XPATH, "//li[span[text()='Grynasis kiekis']]")
        size_and_unit = li_element.find_element(By.XPATH, ".//following-sibling::div[@class='text']//p").text
        self.size = size_and_unit.split()[0]

        # unit
        self.unit = size_and_unit.split()[1]


        # brand
        li_element = self.driver.find_element(By.XPATH, "//li[span[text()='Prekės ženklas']]")
        self.brand = li_element.find_element(By.XPATH, ".//following-sibling::div[@class='text']//p").text


        # price
        try:
            euros = self.driver.find_element(By.CSS_SELECTOR, ".price-wrapper .price span").text
            cents = self.driver.find_element(By.CSS_SELECTOR, ".price-wrapper .price sup").text
            self.price = f"{euros}.{cents}"
        except:
            self.price = None

        print(self.title, self.size, self.unit, self.property, self.brand, self.price)

        # # category
        breadcrumb_elements = self.driver.find_elements(By.CSS_SELECTOR, ".section-header__container p a")
        breadcrumb_items = [breadcrumb.text for breadcrumb in breadcrumb_elements]
        self.category = breadcrumb_items

        # store
        self.store = 2














    # def get_size(self):
    #     return self.driver.find_element(By.XPATH,"/html/body/div[2]/div/div[3]/div/div[3]/div/dl[2]/dd[2]").text