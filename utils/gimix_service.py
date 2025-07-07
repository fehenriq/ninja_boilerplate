import uuid

import requests


class GIMIxService:
    def __init__(self):
        self.base_url = "https://gimix-api.vercel.app/api"

    def send_request(self, endpoint: str, method: str, token: str):
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.request(method, url, headers=headers, timeout=10)
        response.raise_for_status()
        json_response = response.json()

        return json_response

    def get_user_email_by_id(self, user_id: uuid.UUID, token: str):
        endpoint = f"users/{user_id}"
        response = self.send_request(endpoint, "GET", token)
        json_response = response.json()

        return json_response["email"]

    def get_app_admins_email(self, token: str):
        endpoint = "users/emails?is_app_admin=true"
        response = self.send_request(endpoint, "GET", token)

        return response

    def get_users(self, token: str):
        endpoint = "users"
        return self.send_request(endpoint, "GET", token)

    def get_departments(self, token: str):
        endpoint = "departments"
        return self.send_request(endpoint, "GET", token)

    def get_groups(self, token: str):
        endpoint = "groups"
        return self.send_request(endpoint, "GET", token)
