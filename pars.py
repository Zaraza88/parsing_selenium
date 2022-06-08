from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


HOST = 'https://www.dns-shop.ru/'

class SavePages(object):
    """Класс открывает браузер, переходит на нужные страницы и сохраняет их"""

    def __init__(self, driver):
        self.driver = driver

    #запускаем все методы класса
    @classmethod
    def start_selenium(self):
        try:
            self.open_website()
            self.go_to_the_right_page()
            self.save_pages()
        except Exception as ex:
            print(f'---[ERROR]-{ex}-[ERROR]---')
        finally:
            self.driver.close()
            self.driver.quit()
    
    #открываем сайт
    def open_website(self):
        self.driver.get('https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/')
        self.driver.maximize_window()
        sleep(5)

    #переходим на нужный нам город
    def go_to_the_right_page(self):
        self.driver.find_element(By.CLASS_NAME, 'location-icon').click()
        sleep(2)

        self.driver.find_element(By.CLASS_NAME, 'form-control').send_keys('Ростов-на-Дону')
        sleep(4)

        self.driver.find_element(
            By.XPATH, '//*[@id="select-city"]/div[4]/ul[5]/li[4]/a'
        ).click()
        sleep(5)

    #сохраняем первые 3 html страницы 
    def save_pages(self):
        for page in range(3, 6):
            click_on_page = self.driver.find_element(
                By.XPATH, f'//*[@id="products-list-pagination"]/ul/li[{page}]/a'
            )
            click_on_page.click()
            sleep(2)

            with open(f'index_page_{page}.html', 'w') as file:
                result = file.write(self.driver.page_source) 


class ParseContentBlock(object):
    """Класс собирает данные с конкретного блока и сохраняет их"""

    def __init__(self, result):
        self.result = result
    
    @classmethod
    def parse_block(self):
        soup = BeautifulSoup(self.result, 'lxml')

        content_block = soup.find_all(
            'div', class_='catalog-product ui-button-widget'
        )

        for block in content_block:
            try:
                price = block.find('div', class_='product-buy__price').text
                price.replace('₽', '').strip().replace(' ','.')
            except AttributeError:
                continue

            try:
                name = block.find(
                    'a', class_='catalog-product__name ui-link ui-link_black'
                ).text
            except AttributeError:
                continue
            
            try:
                link = HOST + block.find(
                    'a', class_='catalog-product__name ui-link ui-link_black'
                ).get('href')
            except AttributeError:
                continue

            data.append([price, name, link])


class Parsing(object):
    """Запуск парсера"""

    def init_pars(self):
        options = webdriver.ChromeOptions()
        options.add_argument(
            f"user-agent={'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}"
        )

        driver = webdriver.Chrome(
            executable_path='/home/zaraza/Projects/Парсер/parserDB/chromedriver',
            options=options
        )
        SavePages(driver).start_selenium()

    #парсим сохраненный html и сохраняем его в список
    def pars_and_save_data(self):
        global data
        data = []
        #по тз треповалось первые 30 продуктов в порядке возрастания
        data = sorted(data[:30], reverse=True)

        for page in range(3, 6):
            with open(f"index_page_{page}.html") as file:
                result = file.read()
                ParseContentBlock(result).parse_block()
        
        return data


def main():
    asd = Parsing()
    asd.init_pars()
    return asd.pars_and_save_data()
