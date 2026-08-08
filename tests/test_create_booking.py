import allure
import httpx
import pytest
from core.settings.environments import Environment
from core.clients.endpoints import Endpoints
from jsonschema import validate
from .schema.booking_json_schema import BOOKING_SCHEMA


@allure.feature('Создание заказа')
@allure.step('Создание заказа и проверка тела ответа')
def test_create_and_check_response_body(
        api_client,
        generate_random_booking_data
):
    with allure.step('создадим данные для бронирования'):
        body = generate_random_booking_data
    with allure.step('отправим запрос на бронирование'):
        response_json = api_client.create_booking(body)
    with allure.step('Валидация JSON'):
        validate(response_json, BOOKING_SCHEMA)
    with allure.step('Проверка, что ответ содержит переданные данные'):
        for key in body.keys():
            assert response_json['booking'].get(key) == body[key], \
                f'Переданное значение {key} не совпадает с ответом {response_json["booking"].get(key)}'


@allure.feature('Создание заказа')
@allure.step('Создание заказа с пустым телом')
def test_create_booking_with_empty_body(api_client):
    body = {}
    with pytest.raises(httpx.HTTPError):
        api_client.create_booking(body)


@allure.feature('Создание заказа')
@allure.step('Создание заказа без какого либо поля')
@pytest.mark.parametrize(
    'del_key',
    ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates']
)
def test_create_booking_without_any_key(api_client,
                                        generate_random_booking_data,
                                        del_key):
    with allure.step('создадим данные для бронирования'):
        body = generate_random_booking_data
        del body[del_key]
    with pytest.raises(httpx.HTTPError):
        api_client.create_booking(body)


@allure.feature('Создание заказа')
@allure.step('Создание заказа без полей checkin/checkout')
@pytest.mark.parametrize(
    'del_key',
    [
        'checkin', 'checkout'
    ]
)
def test_create_booking_without_booking_date(api_client,
                                             generate_random_booking_data,
                                             del_key):
    with allure.step('создадим данные для бронирования'):
        body = generate_random_booking_data
        del body['bookingdates'][del_key]
    with pytest.raises(httpx.HTTPError):
        api_client.create_booking(body)


@allure.feature('Создание заказа')
@allure.step('Создание заказа c/без депозита(ом)')
@pytest.mark.parametrize('update_value', [True, False])
def test_create_booking_depositpaid(api_client,
                                    generate_random_booking_data,
                                    update_value):
    with allure.step('создадим данные для бронирования'):
        body = generate_random_booking_data
        body['depositpaid'] = update_value
    with allure.step('отправим запрос на бронирование'):
        response_json = api_client.create_booking(body)
    with allure.step('Проверим что в ответе depositpaid содержит переданное значение'):
        assert response_json['booking'].get('depositpaid') == update_value, \
            f"depositpaid в ответе не совпал: отправили {update_value}, вернулось {response_json['booking'].get('depositpaid')}"
