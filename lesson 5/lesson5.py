from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from pprint import pprint

# Создаём вебдрайвер

driver = webdriver.Firefox(executable_path='/usr/local/Cellar/geckodriver/0.29.1/bin/geckodriver')
driver.maximize_window()
driver.get('https://www.mvideo.ru/')

# Создём БД и коллекцию
client = MongoClient('127.0.0.1', 27017)
db = client['mvideo_goods']
mvideo_goods = db.mvideo_goods

# Кликаем на выбор города, печатаем 'Челябинск' в появившемся окне и выбираем его

choose_city_button = driver.find_element_by_id('header-city-selection-link')
choose_city_button.click()

driver.implicitly_wait(10)
city_text_box = driver.find_element_by_id('region-selection-form-city-input')
city_text_box.send_keys('Челябинск')

choose_city_button = driver.find_element_by_class_name('sel-droplist-cities')
choose_city_button.click()

# Скроллим страницу до футера, чтобы всё подгрузить
page = driver.find_element_by_tag_name('html')
page.send_keys(Keys.END)

novinki = driver.find_element_by_xpath('//div[@class = "gallery-title-wrapper"]/h2[contains(text(), "Новинки")]/../../..//ul')
driver.implicitly_wait(10)
driver.execute_script("arguments[0].scrollIntoView();", novinki)
page.send_keys(Keys.ARROW_UP)
page.send_keys(Keys.ARROW_UP)
driver.implicitly_wait(3)
page.send_keys(Keys.ARROW_UP)
page.send_keys(Keys.ARROW_UP)
driver.implicitly_wait(10)
next_button = novinki.find_element_by_xpath('//div[@class = "gallery-title-wrapper"]/h2[contains(text(), "Новинки")]/../../..//ul/../../a[contains(@class, "next-btn")]')

# Нажимаем стрелку вправо, пока она не исчезнет
while 'disabled' not in next_button.get_attribute('class'):
    driver.implicitly_wait(10)
    driver.execute_script("arguments[0].click();", next_button)

mvideo_novinki = driver.find_elements_by_xpath('//div[@class = "gallery-title-wrapper"]/h2[contains(text(), "Новинки")]/../../..//ul/li')

for novinka in mvideo_novinki:
    novinka_dict = {}
    url = novinka.find_element_by_tag_name('a').get_attribute('href')
    title = novinka.find_element_by_tag_name('h3').text
    price = novinka.find_element_by_xpath('//span[contains(@class, "price")]').text

    novinka_dict['url'] = url
    novinka_dict['title'] = title
    novinka_dict['price'] = price

    mvideo_goods.update_one({'url': url}, {'$set': novinka_dict}, upsert = True)

for i in mvideo_goods.find({}):
    pprint(i)
