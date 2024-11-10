import json
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import re


def scrape_hotels(base_url):
    hotels = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto(base_url, timeout=60000)
            page.wait_for_load_state('networkidle')

            page.wait_for_selector('a.Kw61r.vOWh4.KRFSO', timeout=30000)
            links = page.query_selector_all('a.Kw61r.vOWh4.KRFSO')

            hrefs = [link.get_attribute('href') for link in links]
            count = 0

            for href in hrefs:
                if count >= 10:
                    break

                hotel_dict = {}

                if href:
                    absolute_url = urljoin(base_url, href)
                    page.goto(absolute_url, timeout=60000)
                    page.wait_for_load_state('networkidle')

                    # Извлечение данных о названии отеля, изображениях, оценке, описании и цене
                    hotel_name_element = page.query_selector('h1.ReS7e.-hXu6.b9-76')
                    image_elements = page.query_selector_all('img.cRpSH')
                    rating_element = page.query_selector('span._1m7jk.PwvPC.i9Gsh')
                    about_hotel_element = page.query_selector('div.AeeZM.zSvds.uwoF3')
                    price_element = page.query_selector('span.bQcBE[data-qa="price"]')


                    if hotel_name_element:
                        hotel_name = hotel_name_element.text_content().strip()
                        hotel_dict['Название отеля'] = f'{hotel_name}'

                    image_urls = [img.get_attribute('src') for img in image_elements[:2]]
                    if image_urls:
                        hotel_dict['Ссылка на изображение'] = f'{image_urls}'

                    if rating_element:
                        rating = rating_element.text_content().strip()
                        hotel_dict['Оценка'] = f'{rating}'

                    if about_hotel_element:
                        about_hotel = about_hotel_element.text_content().strip()
                        hotel_dict['О отеле'] = f'{about_hotel}'

                    if price_element:
                        price = price_element.text_content().strip().replace('&nbsp;', '').replace('от', '').strip()
                        hotel_dict['Цена'] = price
                    else:
                        hotel_dict['Цена'] = 'Не указана'


                    hotels.append(hotel_dict)

                    page.go_back(timeout=60000)
                    page.wait_for_load_state('networkidle')
                    count += 1

        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            browser.close()

    return hotels


# Функция для сохранения данных в JSON-файл
def save_to_json(data, filename='hotels_data.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении данных в JSON: {e}")


base_url = 'https://travel.yandex.ru/hotels/moscow'

hotels = scrape_hotels(base_url)

save_to_json(hotels)
