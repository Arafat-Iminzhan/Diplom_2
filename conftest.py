import pytest
import requests
from helpers import create_user_data
from data import APILinks

@pytest.fixture(scope="function")
def create_and_delete_user():
    payload = create_user_data()
    login_data = payload.copy()
    del login_data["name"]

    # Отправляем JSON, а не form-data
    response = requests.post(APILinks.MAIN_URL + APILinks.REGISTER_URL, json=payload)

    # Проверка наличия токена в ответе
    if "accessToken" not in response.json():
        print("\n❌ Ошибка регистрации:")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        assert False, "Регистрация не удалась — нет accessToken"

    token = response.json()["accessToken"]

    yield response, payload, login_data, token

    # Удаление пользователя после теста
    requests.delete(APILinks.MAIN_URL + APILinks.USER_URL, headers={"Authorization": token})
