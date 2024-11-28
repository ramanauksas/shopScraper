from selenium.webdriver.common.by import By
from page_objects.product import Product


class BarboraProduct(Product):
    def __init__(self, driver):
        super().__init__(driver)

    def fill(self, url_id):

        # store
        self.store = 1

        try:
            title_text_full = self.driver.find_element(By.CLASS_NAME, "b-product-info--title").text
        except:
            print("Produktas nerastas")
            return None
        title_parts = title_text_full.split(",")
        # title
        self.title = title_parts[0]

        # size
        self.size = title_parts[-1].split()[0]

        # unit
        try:
            self.unit = title_parts[-1].split()[1]
        except:
            return None


        # property
        if len(title_parts)>2:
            self.property = ",".join(title_parts[1:-1])

        # brand
        try:
            dt_element = self.driver.find_element(By.XPATH, "//dt[text()='Prekės ženklas:']")
            self.brand = dt_element.find_element(By.XPATH, "following-sibling::dd").text
        except:
            print("failed to determine product brand")
            pass
        # price
        price_element = self.driver.find_element(By.ID, "fti-product-price--0")
        price_parts = price_element.find_elements(By.TAG_NAME, "span")
        whole_number = price_parts[0].text.strip()
        decimal_part = price_parts[2].text.strip()
        self.price = f"{whole_number}.{decimal_part}"

        # category
        breadcrumb_items = self.driver.find_elements(By.CSS_SELECTOR, "ol.breadcrumb li span[itemprop='name']")
        category_list = [item.text for item in breadcrumb_items][1:]
        self.save_category(category_list)
        print(category_list)
        print(self.category)


        self.link = url_id














    # def get_size(self):
    #     return self.driver.find_element(By.XPATH,"/html/body/div[2]/div/div[3]/div/div[3]/div/dl[2]/dd[2]").text