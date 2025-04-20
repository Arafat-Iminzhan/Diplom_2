import pytest
import allure
import requests
from conftest import create_and_delete_user
from data import APILinks
from helpers import generate_random_string


class TestChangeUserData:

    @allure.title('Успешное изменение почты авторизованного пользователя')
    def test_change_user_email_authorised_user_success(self, create_and_delete_user):
        new_email = f'{generate_random_string(5)}@yandex.ru'
        payload = {'email': new_email}
        token = {'Authorization': create_and_delete_user[3]}

        with allure.step("Отправка PATCH-запроса на изменение email"):
            response = requests.patch(APILinks.MAIN_URL + APILinks.USER_URL, headers=token, data=payload)

        with allure.step("Проверка ответа: статус 200 и email изменён"):
            assert response.status_code == 200
            assert response.json()['user']['email'] == new_email

    @allure.title('Успешное изменение пароля авторизованного пользователя')
    def test_change_user_password_authorised_user_success(self, create_and_delete_user):
        new_password = generate_random_string(5)
        payload = {'password': new_password}
        token = {'Authorization': create_and_delete_user[3]}

        with allure.step("Отправка PATCH-запроса на изменение пароля"):
            response = requests.patch(APILinks.MAIN_URL + APILinks.USER_URL, headers=token, data=payload)

        with allure.step("Проверка ответа: статус 200 и success True"):
            assert response.status_code == 200
            assert response.json().get("success") is True

    @allure.title('Успешное изменение имени авторизованного пользователя')
    def test_change_user_name_authorised_user_success(self, create_and_delete_user):
        new_name = generate_random_string(5)
        payload = {'name': new_name}
        token = {'Authorization': create_and_delete_user[3]}

        with allure.step("Отправка PATCH-запроса на изменение имени"):
            response = requests.patch(APILinks.MAIN_URL + APILinks.USER_URL, headers=token, data=payload)

        with allure.step("Проверка ответа: статус 200 и имя изменено"):
            assert response.status_code == 200
            assert response.json()['user']['name'] == new_name

    @allure.title('Ошибка при изменении данных неавторизованного пользователя')
    @pytest.mark.parametrize('payload', [
        {'email': f'{generate_random_string(5)}@yandex.ru'},
        {'password': generate_random_string(5)},
        {'name': generate_random_string(5)}
    ])
    def test_change_user_data_without_authorization_fail(self, payload):
        with allure.step("Попытка изменить данные без авторизации"):
            response = requests.patch(APILinks.MAIN_URL + APILinks.USER_URL, data=payload)

        with allure.step("Проверка ответа: статус 401 и сообщение об ошибке авторизации"):
            assert response.status_code == 401
            assert response.json()['message'] == 'You should be authorised'
