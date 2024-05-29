import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .models import CurrencyRate
"""
Так как id для валют с двух сайтов не совпадают,
то задаем требуемые id вручную. Не совсем адаптивно :(
"""




CURRENCY_CODES = {
    'USD': 52148,
    'EUR': 52170,
    'GBP': 52146,
    'TRY': 52158,
    'JPY': 52246,
    'INR': 52238,
    'CNY': 52207
}

def fetch_currency_rates(start_date, end_date):
    all_data = []
    for currency, code in CURRENCY_CODES.items():
        url = f"https://www.finmarket.ru/currency/rates/?id=10148&pv=1&cur={code}&bd={start_date.day}&bm={start_date.month}&by={start_date.year}&ed={end_date.day}&em={end_date.month}&ey={end_date.year}#archive"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table', class_='karramba')
        for row in table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            date = datetime.strptime(cols[0].text.strip(), '%d.%m.%Y').date()
            rate = float(cols[2].text.strip().replace(',', '.'))
            change = float(cols[3].text.strip().replace(',', '.'))
            currency_code = code
            all_data.append({'date': date, 'currency': currency, 'rate': rate, 'change': change, 'currency_code': currency_code})
    return all_data

def fetch_country_currencies():
    url = "https://www.iban.ru/currency-codes"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    table = soup.find('table', class_='table table-bordered downloads tablesorter')
    data = []

    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        country = cols[0].text.strip()
        currency_name = cols[1].text.strip()
        currency_code = cols[2].text.strip()
        currency_number = int(cols[3].text.strip()) if cols[3].text.strip() != '' else 0
        data.append({'country': country, 'currency_name': currency_name, 'currency_code': currency_code, 'currency_number': currency_number})

    return data


def calculate_relative_changes(base_date):
    base_rates = CurrencyRate.objects.filter(date=base_date)
    relative_changes = []
    print(base_date)
    for base_rate in base_rates:
        print('asdasd')
        currency = base_rate.currency
        rates = CurrencyRate.objects.filter(currency=currency)
        for rate in rates:
            relative_change = (rate.rate - base_rate.rate) / base_rate.rate * 100 ### НАНИ?
            relative_changes.append({
                'date': rate.date,
                'currency': currency,
                'relative_change': relative_change,
                'relative_date': base_date
            })

    return relative_changes