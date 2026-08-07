import allure
import pytest
from core.settings.environments import Environment
from core.clients.endpoints import Endpoints
from jsonschema import validate
from .schema.booking_json_schema import BOOKING_SCHEMA


@allure.feature('Создание заказа')
@allure.step('Создание заказа')
def test_create_booking(api_client, generate_random_booking_data):
    url = api_client.get_base_url(Environment.PROD)
    data = generate_random_booking_data
    with allure.step('отправляем запрос'):
        response = api_client.session.post(f'{url}/{Endpoints.BOOKING_ENDPOINT.value}', json=data)
        response_json = response.json()
    with allure.step('проверяем статус код'):
        assert response.status_code == 200, f"статус код не совпадает, ожидали 200, пришел {response.status_code}"
    with allure.step('проверим что id есть в ответе и оно целое число'):
        assert isinstance(response_json.get('bookingid'), int), \
            f"bookingid не число или отсутствует, пришло: {response_json.get('bookingid')}"


@allure.feature('Создание заказа')
@allure.step('Проверка тела ответа')
def test_response_body(api_client, generate_random_booking_data):
    url = api_client.get_base_url(Environment.PROD)
    data = generate_random_booking_data
    with allure.step('отправляем запрос'):
        response = api_client.session.post(f'{url}/{Endpoints.BOOKING_ENDPOINT.value}', json=data)
        response_json = response.json()
    with allure.step('проверяем статус код'):
        assert response.status_code == 200, f"статус код не совпадает, ожидали 200, пришел {response.status_code}"
    with allure.step('Валидация JSON'):
        validate(response_json, BOOKING_SCHEMA)
    with allure.step('Проверка, что ответ содержит переданные данные'):
        for key in data.keys():
            assert response_json['booking'].get(key) == data[key], \
                f'Переданное значение {key} не совпадает с ответом {response_json["booking"].get(key)}'


@allure.feature('Создание заказа')
@allure.step('Создание заказа с пустым телом')
def test_create_booking_with_empty_body(api_client):
    url = api_client.get_base_url(Environment.PROD)
    data = {}
    with allure.step('отправляем запрос'):
        response = api_client.session.post(f'{url}/{Endpoints.BOOKING_ENDPOINT.value}', json=data)
    with allure.step('проверяем статус код'):
        assert response.status_code == 500, \
            f"статус код не совпадает, ожидали 500, пришел {response.status_code}"


@allure.feature('Создание заказа')
@allure.step('Создание заказа без какого либо поля')
@pytest.mark.parametrize(
    'del_key, expected_status_code',
    [
        ('firstname', 500),
        ('lastname', 500),
        ('totalprice', 500),
        ('depositpaid', 500),
        ('bookingdates', 500),
        ('additionalneeds', 200)
    ]
)
def test_create_booking_without_any_key(api_client, generate_random_booking_data, del_key, expected_status_code):
    url = api_client.get_base_url(Environment.PROD)
    data = generate_random_booking_data
    del data[del_key]
    with allure.step('отправляем запрос'):
        response = api_client.session.post(f'{url}/{Endpoints.BOOKING_ENDPOINT.value}', json=data)
    with allure.step('проверяем статус код'):
        assert response.status_code == expected_status_code, \
            f"статус код не совпадает, ожидали {expected_status_code}, пришел {response.status_code}"


@allure.feature('Создание заказа')
@allure.step('Создание заказа без полей checkin/checkout')
@pytest.mark.parametrize(
    'del_key, expected_status_code',
    [
        ('checkin', 500),
        ('checkout', 500),
    ]
)
def test_create_booking_without_booking_date(api_client, generate_random_booking_data, del_key, expected_status_code):
    url = api_client.get_base_url(Environment.PROD)
    data = generate_random_booking_data
    del data['bookingdates'][del_key]
    with allure.step('отправляем запрос'):
        response = api_client.session.post(f'{url}/{Endpoints.BOOKING_ENDPOINT.value}', json=data)
    with allure.step('проверяем статус код'):
        assert response.status_code == expected_status_code, \
            f"статус код не совпадает, ожидали {expected_status_code}, пришел {response.status_code}"


@allure.feature('Создание заказа')
@allure.step('Создание заказа c/без депозитом')
@pytest.mark.parametrize(
    'update_value, expected_status_code',
    [
        (True, 200),
        (False, 200),
    ]
)
def test_create_booking_depositpaid(api_client, generate_random_booking_data, update_value, expected_status_code):
    url = api_client.get_base_url(Environment.PROD)
    data = generate_random_booking_data
    data['depositpaid'] = update_value
    with allure.step('отправляем запрос'):
        response = api_client.session.post(f'{url}/{Endpoints.BOOKING_ENDPOINT.value}', json=data)
    with allure.step('проверяем статус код'):
        assert response.status_code == expected_status_code, \
            f"статус код не совпадает, ожидали {expected_status_code}, пришел {response.status_code}"
