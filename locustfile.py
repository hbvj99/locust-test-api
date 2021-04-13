import time

from locust import HttpUser, task, between

from credentails import email, password


class MarketAPI(HttpUser):
    wait_time = between(0, 1.9)
    base_api_version = 'api/v1'

    def on_start(self):
        self.login()

    @task(1)
    def login(self):
        response = self.client.post(f"{self.base_api_version}/auth/token/", json={"email": email, "password": password})
        if response.json().get('errors'):
            print(response.text)
        self.access_token = response.json()['access']
        self.refresh_token = response.json()['refresh']

    @task(2)
    def list_items(self):
        if response.json().get('errors'):
            print(response.text)
        self.client.get(f"{self.base_api_version}/products/", headers={'Authorization': f'Bearer {self.access_token}'})
        self.client.get(f"{self.base_api_version}/products/comments/", headers={'Authorization': f'Bearer {self.access_token}'})


    @task(3)
    def view_products(self):
        if response.json().get('errors'):
            print(response.text)
        for product in range(1, 3):
            self.client.get(f"{self.base_api_version}/products/{product}/",
                            headers={'Authorization': f'Bearer {self.access_token}'})
            time.sleep(0.3)

    @task(4)
    def refresh_token(self):
        if response.json().get('errors'):
            print(response.text)
        new_refresh_token = self.client.post(f"{self.base_api_version}/auth/token/refresh/",
                         json={"refresh": self.refresh_token},
                         headers={'Authorization': f'Bearer {self.access_token}'})
        print(new_refresh_token.text)