import requests
from decouple import config

def get_city_from_ip(ip_address):
    api_key = config('API_KEY')
    url = f"http://api.ipstack.com/{ip_address}"
    params = {
        'access_key': api_key,
        'format': 1  # sets JSON format
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        city = data.get('city')
        if city:
            return city
    return " your city"
