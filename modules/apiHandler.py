import requests
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class APIHandler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=1,
                        status_forcelist=[502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def send_request(self, endpoint, method='GET', data=None, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method=method, url=url, json=data, params=params, headers=headers)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}') 
        except Exception as err:
            logging.error(f'Other error occurred: {err}')
        return None


