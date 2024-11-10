import json
from playwright.sync_api import sync_playwright

# Функция для парсинга данных о рейсах с веб-сайта
def scrape_flights(base_url):
    flights = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = context.new_page()

        try:
            page.goto(base_url, timeout=120000) 
            page.wait_for_load_state('networkidle', timeout=120000)


            page_0_elements = page.query_selector_all('li.page_0')


            for element in page_0_elements:
                flight_dict = {}


                flight_number_element = element.query_selector('.flightNumber')
                if flight_number_element:
                    flight_number = flight_number_element.text_content().strip()
                    flight_dict['Номер рейса'] = flight_number

                flight_status_element = element.query_selector('.flightstatus')
                if flight_status_element:
                    flight_status = flight_status_element.text_content().strip()
                    flight_dict['Статус рейса'] = flight_status

                if flight_dict:
                    flights.append(flight_dict)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            browser.close()

    # Возвращаем список рейсов
    return flights


def save_to_json(data, filename='flights_data.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении данных в JSON: {e}")


def main():
    arrival_url = 'https://m.dme.ru/passengers/flight/live-board/?Direction=A&searchtext='
    departure_url = 'https://m.dme.ru/passengers/flight/live-board/?Direction=D&searchtext='

    arrival_flights = scrape_flights(arrival_url)
    departure_flights = scrape_flights(departure_url)

    all_flights = {
        'arrivals': arrival_flights,
        'departures': departure_flights
    }

    save_to_json(all_flights)


if __name__ == "__main__":
    main()
