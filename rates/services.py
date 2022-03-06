"""Module to retrieve exchange rates from three different sources"""
import http.client
from datetime import datetime
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from django.conf import settings


def retrieve_dof():
    """Scrapes DOF website and returns a new dict"""
    response = requests.get(settings.URL_DOF)
    if response.status_code != http.client.OK:
        return {}
    if 'html' not in response.headers['Content-type']:
        return {}

    page = BeautifulSoup(response.text, 'html.parser')
    row = page.find('tr', class_='renglonNon')
    date, *_, value = row.find_all('td');

    last_updated = datetime.strptime(date.text.strip(), "%d/%m/%Y")
    return {
        'last_updated': last_updated.isoformat(),
        'value': Decimal(value.text.strip()),
    }


def retrieve_banxico():
    """Makes a request to Banxico and returns a new dict"""
    today = datetime.today().strftime('%Y-%m-%d')
    response = requests.get(f'{settings.URL_BANXICO}{today}/{today}',
            headers={'Bmx-Token': settings.BANXICO_KEY})
    if response.status_code != http.client.OK:
        return {}
    try:
        data = response.json()['bmx']['series'][0]['datos'][0]
    except KeyError:
        return {}
    except requests.exceptions.JSONDecodeError:
        return {}

    last_updated = datetime.strptime(data['fecha'], "%d/%m/%Y")
    return {
        'last_updated': last_updated.isoformat(),
        'value': Decimal(data['dato']),
    }

def retrieve_fixer():
    """Makes a request to Fixer and returns a new dict"""
    response = requests.get(f'{settings.URL_FIXER}?access_key={settings.FIXER_KEY}&symbols=MXN')
    if response.status_code != http.client.OK:
        return {}
    data = response.json()
    if not data['success']:
        return {}
    last_updated = datetime.strptime(data['date'], "%Y-%m-%d")
    return {
        'last_updated': last_updated.isoformat(),
        'value': Decimal(data['rates']['MXN']).quantize(Decimal(10) ** -4),
    }
