import pytest
import requests
import logging
import allure
from helpers import create_user_data
from data import APILinks

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def create_and_delete_user():
    payload = create_user_data()
    login_data = payload.copy()
    del login_data["name"]

    with allure.step("Регистрация пользователя через POST-запрос"):
        response = requests.post(APILinks.MAIN_URL + APILinks.REGISTER_URL, json=payload)

    if "accessToken" not in response.json():
        logger.error("❌ Ошибка регистрации:")
        logger.error(f"Status Code: {response.status_code}")
        logger.error(f"Response: {response.text}")
        assert False, "Регистрация не удалась — нет accessToken"

    token = response.json()["accessToken"]

    yield response, payload, login_data, token

    with allure.step("Удаление пользователя через DELETE-запрос"):
        requests.delete(APILinks.MAIN_URL + APILinks.USER_URL, headers={"Authorization": token})
