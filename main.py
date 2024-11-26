from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from scrapers.barbora_scraper import BarboraScraper
from scrapers.rimi_scraper import  RimiScraper

def initialize_webdriver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def run_data_scraping():
    driver, wait = initialize_webdriver()
    # scraper = BarboraScraper(driver, "https://barbora.lt/gerimai/alus/sviesusis-alus")
    scraper = BarboraScraper(driver, "https://barbora.lt")
    # scraper = RimiScraper(driver, wait,"https://www.rimi.lt/e-parduotuve/lt/produktai/bakaleja/kruopos/grikiai/c/SH-2-6-36")
    # scraper = RimiScraper(driver, wait,"https://www.rimi.lt/e-parduotuve/lt/produktai/alkoholiniai-ir-nealkoholiniai-gerimai/alus/sviesus-alus/c/SH-1-1-4")


    scraper.scrape_data()

run_data_scraping()
