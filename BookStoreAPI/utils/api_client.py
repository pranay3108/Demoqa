import requests
import logging
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url, headers):
        self.base_url = base_url.rstrip("/") + "/"
        self.session = requests.Session()
        self.session.headers.update(headers)

    def _log_response(self, response):
        logger.info(f"Request: {response.request.method} {response.request.url}")
        logger.info(f"Response Status: {response.status_code}")
        if response.text:
            logger.debug(f"Response Body: {response.text}")

    def get(self, endpoint, params=None):
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        response = self.session.get(url, params=params)
        self._log_response(response)
        return response

    def post(self, endpoint, data=None, json=None):
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        response = self.session.post(url, data=data, json=json)
        self._log_response(response)
        return response

    def put(self, endpoint, data=None, json=None):
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        response = self.session.put(url, data=data, json=json)
        self._log_response(response)
        return response

    def delete(self, endpoint, **kwargs):
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        response = self.session.delete(url, **kwargs)
        self._log_response(response)
        return response