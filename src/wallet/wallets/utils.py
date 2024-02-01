import requests
from django.conf import settings


def request_third_party_deposit():
    bank_api_url = settings.BANK_API_URL
    response = requests.post(bank_api_url)
    return response.json()
