import allure
import requests
from conftest import create_and_delete_user
from data import APILinks
from helpers import create_user_login


class TestLoginUser:

    @allure.title('Успешная авторизация пользователя')
    def test_user_login_success(self, create_and_delete_user):
        with allure.step("Отправка POST-запроса на логин с валидными данными"):
            response = requests.post(
                APILinks.MAIN_URL + APILinks.LOGIN_URL,
                data=create_and_delete_user[2]
            )

        with allure.step("Проверка: статус 200 и success=True"):
            assert response.status_code == 200
            assert response.json().get("success") is True

    @allure.title('Ошибка при авторизации с неверным логином и паролем')
    def test_user_login_incorrect_login_data_fail(self):
        with allure.step("Генерация случайных несуществующих данных логина"):
            payload = create_user_login()

        with allure.step("Отправка POST-запроса на логин с некорректными данными"):
            response = requests.post(APILinks.MAIN_URL + APILinks.LOGIN_URL, data=payload)

        with allure.step("Проверка: статус 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()['message'] == "email or password are incorrect"
