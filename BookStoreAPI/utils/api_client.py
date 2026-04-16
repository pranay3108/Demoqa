import requests
from urllib.parse import urljoin

class APIClient:
    def __init__(self, base_url, headers):
        self.base_url = base_url.rstrip("/") + "/"
        self.session = requests.Session()
        self.session.headers.update(headers)

    def get(self, endpoint):
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        return self.session.get(url)

    def post(self, endpoint, data=None, json=None):
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        return self.session.post(url, data=data, json=json)

    def delete(self, endpoint):
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        return self.session.delete(url)