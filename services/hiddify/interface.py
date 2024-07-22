import datetime
import json

import requests


class HiddifyInterface:
    def __init__(self, url: str, proxy_path: str, users_path: str, admin_uuid: str) -> None:
        self._url = url
        self._proxy_path = proxy_path
        self._users_path = users_path
        self._admin_uuid = admin_uuid
        self._complete_url = self._url + '/' + self._proxy_path
        self._headers = {
            'Content-Type': "application/json",
            'Accept': "application/json",
            'Hiddify-API-Key': self._admin_uuid
        }

    def create_service(self, name: str, days: int, limit: int):
        payload = {
            "enable": True,
            "is_active": True,
            "mode": "no_reset",
            "name": name,
            "package_days": days,
            "start_date": datetime.date.today().strftime("%Y-%m-%d"),
            "usage_limit_GB": limit,
        }

        response = requests.post(self._complete_url + '/api/v2/admin/user/', headers=self._headers,
                                 data=json.dumps(payload))

        return json.loads(response.text)

    def delete_service(self, uuid: str):
        response = requests.delete(self._complete_url + f'/api/v2/admin/user/{uuid}/', headers=self._headers)
        return json.loads(response.text)

    def get_service(self, uuid: str):
        response = requests.get(self._complete_url + f'/api/v2/admin/user/{uuid}/', headers=self._headers)

        return json.loads(response.text) if response.status_code != 404 else None

    def get_services(self):
        response = requests.get(self._complete_url + '/api/v2/admin/user/', headers=self._headers)
        return json.loads(response.text)

    def prolong_service(self, uuid: str):
        payload = {
            "current_usage_GB": 0,
            "start_date": datetime.date.today().strftime("%Y-%m-%d"),
        }
        response = requests.patch(self._complete_url + f'/api/v2/admin/user/{uuid}/', headers=self._headers,
                                  data=json.dumps(payload))
        return json.loads(response.text)

    def get_sub_link(self, uuid: str):
        return f"{self._url}/{self._users_path}/{uuid}/"
