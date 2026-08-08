from datetime import datetime, timedelta
from faker import Faker
import pytest
from core.clients.api_client import APIClient
from core.settings.environments import Environment
from core.clients.endpoints import Endpoints


@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    client.auth()
    return client


@pytest.fixture()
def booking_dates():
    today = datetime.today()
    checkin_data = today + timedelta(days=10)
    checkout_data = checkin_data + timedelta(days=5)

    return {
        'checkin': checkin_data.strftime('%Y-%m-%d'),
        'checkout': checkout_data.strftime('%Y-%m-%d')
    }


@pytest.fixture()
def generate_random_booking_data(booking_dates):
    faker = Faker()
    firstname = faker.first_name()
    lastname = faker.last_name()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()
    additionalneeds = faker.sentence()

    data = {
        'firstname': firstname,
        'lastname': lastname,
        'totalprice': totalprice,
        'depositpaid': depositpaid,
        'bookingdates': booking_dates,
        'additionalneeds': additionalneeds

    }
    return data


@pytest.fixture()
def booking_url(api_client):
    url = api_client.get_base_url(Environment.PROD)
    return f'{url}/{Endpoints.BOOKING_ENDPOINT.value}'
