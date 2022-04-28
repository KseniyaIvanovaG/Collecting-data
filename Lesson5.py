from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint

options = Options()
options.add_argument("start-maximized")

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)

driver.get('https://www.mvideo.ru/')
driver.execute_script("window.scrollTo(0, 800)")
driver.find_element(By.XPATH, "//button[@class='tab-button ng-star-inserted']").click()

goods = driver.find_elements(By.XPATH, "//mvid-product-cards-group[@style='grid-template-columns: repeat(16, 20rem);]")
goods_list = []
for item in goods:
    goods_info = {}
    goods_name = item.find_element(By.XPATH, ".//a[@class='ng-star-inserted']").text
    goods_info['name'] = goods_name

    goods_list.append(goods_info)

pprint(goods_list)

