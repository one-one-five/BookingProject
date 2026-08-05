import httpx
import os
from dotenv import load_dotenv
from core.settings.environments import Environment
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts
from httpx import BasicAuth
import allure

load_dotenv()


class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f'Unsupported environment value: {environment_str}')

        self.base_url = self.get_base_url(environment)
        self.session = httpx.Client()
        self.session.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_base_url(self, environment: Environment):
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f'Unsupported environment value: {environment}')

    def ping(self):
        with allure.step('Ping api client'):
            url = f'{self.base_url}/{Endpoints.PING_ENDPOINT}'
            response = self.session.get(url)
            response.raise_for_status()

        with allure.step('Assert status code'):
            assert response.status_code == 201, f'Expected status 201 got {response.status_code}'
        return response.status_code

    def auth(self):
        with allure.step('Getting authenticate'):
            url = f'{self.base_url}/{Endpoints.AUTH_ENDPOINT}'
            data = {
                "username": Users.USERNAME,
                "password": Users.PASSWORD
            }
            response = self.session.post(url, json=data, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()

        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        token = response.json().get('token')

        with allure.step('Setting auth cookie'):
            self.session.cookies.update({'token': token})

    def get_bookings_id(self, params=None):
        with allure.step('Отправляем запрос'):
            url = f'{self.base_url}/{Endpoints.BOOKING_ENDPOINT}'
            response = self.session.get(url, params=params, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'

        all_bookings_id = response.json()
        booking_ids = [item['bookingid'] for item in all_bookings_id]
        return booking_ids

    def get_booking_by_id(self, booking_id):
        with allure.step('Отправляем запрос'):
            url = f'{self.base_url}/{Endpoints.BOOKING_ENDPOINT}/{booking_id}'
            response = self.session.get(url, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()

    def create_booking(self, booking_data):
        with allure.step('Отправляем запрос'):
            url = f'{self.base_url}/{Endpoints.BOOKING_ENDPOINT}'
            response = self.session.post(url, json=booking_data)
            response.raise_for_status()
        with allure.step('Проверяем статус код'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()

    def update_booking(self, booking_data, booking_id, auth=None):
        with allure.step('Отправляем запрос'):
            url = f'{self.base_url}/{Endpoints.BOOKING_ENDPOINT}/{booking_id}'
            response = self.session.put(url, json=booking_data, auth=auth)
            response.raise_for_status()
        with allure.step('Проверяем статус код'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()

    def partial_update_booking(self, booking_data, booking_id, auth=None):
        with allure.step('Отправляем запрос'):
            url = f'{self.base_url}/{Endpoints.BOOKING_ENDPOINT}/{booking_id}'
            response = self.session.patch(url, json=booking_data, auth=auth)
            response.raise_for_status()
        with allure.step('Проверяем статус код'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()

    def delete_booking(self, booking_id, auth=None):
        with allure.step('Отправляем запрос'):
            url = f'{self.base_url}/{Endpoints.BOOKING_ENDPOINT}/{booking_id}'
            response = self.session.delete(url, auth=auth)
            response.raise_for_status()
        with allure.step('Проверяем статус код'):
            assert response.status_code == 201, f'Expected status 201 but got {response.status_code}'
        return response.status_code
