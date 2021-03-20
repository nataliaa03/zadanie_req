import requests
import pytest
import json
from test_data import BASE_URL


class RequestsMethods:

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}

    def get_apps(self, offset, limit, search=None): #in this method search=None by deafult (this paramter is not passe by defaultin tests)
        payload = {'offset': offset, 'limit': limit, 'search': search}
        response = requests.get(url=BASE_URL, headers=self.headers, params=payload)
        return response

    def get_app_by_id(self, id):
        response = requests.get(url=BASE_URL+id, headers=self.headers)
        return response

    def del_app_by_id(self, id):
        response = requests.delete(BASE_URL+id)
        return response

    def create_app(self, payload):
        request_json = json.loads(payload)
        response = requests.post(url=BASE_URL, json=request_json)
        return response

    def patch_app_by_id(self, id, payload):
        request_json = json.loads(payload)
        response = requests.patch(url=BASE_URL+id, headers=self.headers, json=request_json)
        return response
