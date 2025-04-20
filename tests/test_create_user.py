import pytest
import allure
import requests
from conftest import create_and_delete_user
from data import APILinks, UserData
from helpers import create_user_data


class TestCreateUser:

    @allure.title('Успешная регистрация нового пользователя')
    def test_create_new_user_success(self, create_and_delete_user):
        payload = create_user_data()

        with allure.step("Отправка POST-запроса на регистрацию нового пользователя"):
            response = requests.post(APILinks.MAIN_URL + APILinks.REGISTER_URL, data=payload)

        with allure.step("Проверка ответа: статус 200 и success=True"):
            assert response.status_code == 200
            assert response.json().get("success") is True

    @allure.title('Ошибка при создании пользователя с уже зарегистрированным email')
    def test_create_user_with_duplicate_data_fail(self, create_and_delete_user):
        with allure.step("Отправка POST-запроса с уже существующими данными"):
            response = requests.post(APILinks.MAIN_URL + APILinks.REGISTER_URL, data=create_and_delete_user[1])

        with allure.step("Проверка ответа: статус 403 и сообщение 'User already exists'"):
            assert response.status_code == 403
            assert response.json()['message'] == "User already exists"

    @allure.title('Ошибка при создании пользователя без обязательных полей')
    @pytest.mark.parametrize('payload', (
        UserData.without_name,
        UserData.without_email,
        UserData.without_password
    ))
    def test_create_user_without_required_fields_fail(self, payload):
        with allure.step(f"Отправка POST-запроса с неполными данными: {payload}"):
            response = requests.post(APILinks.MAIN_URL + APILinks.REGISTER_URL, data=payload)

        with allure.step("Проверка ответа: статус 403 и сообщение об обязательных полях"):
            assert response.status_code == 403
            assert response.json()['message'] == "Email, password and name are required fields"
