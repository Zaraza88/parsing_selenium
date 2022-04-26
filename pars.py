from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


HOST = 'https://www.dns-shop.ru/'


def get_original_html_and_save():
    """Получаем штмл и сохраняем его для дальнейшей обработки"""

    options = webdriver.ChromeOptions()
    options.add_argument(
        f"user-agent={'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}"
    )

    try:
        driver = webdriver.Chrome(
            executable_path='/home/zaraza/Projects/Парсер/parserDB/chromedriver',
            options=options,
        )
        driver.get(
            url='https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/'
        )
        driver.maximize_window()
        sleep(5)

        click_on_the_city = driver.find_element(By.CLASS_NAME, 'location-icon').click()
        sleep(2)

        city_input = driver.find_element(By.CLASS_NAME, 'form-control')
        sleep(1)
        city_input.send_keys('Ростов-на-Дону')
        sleep(4)

        click_on_selected_city = driver.find_element(
            By.XPATH, '//*[@id="select-city"]/div[4]/ul[5]/li[4]/a'
        ).click()
        sleep(5)
    
        #сохраняем каждую страницу в отдельный файл
        for page in range(3, 6):

            click_on_page = driver.find_element(
                By.XPATH, f'//*[@id="products-list-pagination"]/ul/li[{page}]/a'
            )
            click_on_page.click()
            sleep(2)

            with open(f'index_page_{page}.html', 'w') as file:
                result = file.write(driver.page_source)      

    except Exception as ex:
        print(f'[ERROR] {ex} [ERROR]')

    finally:
        driver.close()
        driver.quit()


def parse_content_block(result):
    """Парсим каждый блок продукта"""

    soup = BeautifulSoup(result, 'lxml')

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


def parse():

    global data
    data = []
    data = sorted(data[:30], reverse=True)

    get_original_html_and_save()

    for page in range(3, 6):
        with open(f"index_page_{page}.html") as file:
            result = file.read()
            parse_content_block(result)

    return data
