import allure
import requests
from conftest import create_and_delete_user
from data import APILinks, IngredientsData


class TestCreateOrder:

    @allure.title('Успешное создание заказа авторизованным пользователем')
    def test_create_order_authorised_user_success(self, create_and_delete_user):
        token = {'Authorization': create_and_delete_user[3]}

        with allure.step("Отправляем POST-запрос на создание заказа с авторизацией"):
            response = requests.post(APILinks.MAIN_URL + APILinks.ORDERS_URL, headers=token,
                                     data=IngredientsData.correct_ingredients)

        with allure.step("Проверяем, что заказ успешно создан"):
            assert response.status_code == 200
            assert response.json().get("success") is True

    @allure.title('Успешное создание заказа неавторизованным пользователем')
    def test_create_order_user_without_authorisation_success(self):
        with allure.step("Отправляем POST-запрос на создание заказа без авторизации"):
            response = requests.post(APILinks.MAIN_URL + APILinks.ORDERS_URL,
                                     data=IngredientsData.correct_ingredients)

        with allure.step("Проверяем, что заказ успешно создан"):
            assert response.status_code == 200
            assert response.json().get("success") is True

    @allure.title('Ошибка при создании заказа без ингредиентов')
    def test_create_order_without_ingredients_fail(self):
        with allure.step("Отправляем POST-запрос без ингредиентов"):
            response = requests.post(APILinks.MAIN_URL + APILinks.ORDERS_URL)

        with allure.step("Проверяем, что вернулась ошибка 400 и соответствующее сообщение"):
            assert response.status_code == 400
            assert response.json()['message'] == "Ingredient ids must be provided"

    @allure.title('Ошибка при создании заказа c неверным хешем ингредиентов')
    def test_create_order_incorrect_hash_fail(self):
        with allure.step("Отправляем POST-запрос с неверными ингредиентами"):
            response = requests.post(APILinks.MAIN_URL + APILinks.ORDERS_URL,
                                     data=IngredientsData.incorrect_ingredients)

        with allure.step("Проверяем, что вернулась ошибка 500 и текст 'Internal Server Error'"):
            assert response.status_code == 500
            assert 'Internal Server Error' in response.text
