import allure
import requests
from conftest import create_and_delete_user
from data import APILinks, IngredientsData


class TestGetOrder:

    @allure.title('Успешное получение заказа авторизованным пользователем')
    def test_get_order_with_authorised_user_success(self, create_and_delete_user):
        token = {'Authorization': create_and_delete_user[3]}

        with allure.step("Создание заказа с валидными ингредиентами"):
            create_response = requests.post(
                APILinks.MAIN_URL + APILinks.ORDERS_URL,
                headers=token,
                data=IngredientsData.correct_ingredients
            )

        with allure.step("Запрос списка заказов авторизованного пользователя"):
            get_response = requests.get(
                APILinks.MAIN_URL + APILinks.ORDERS_URL,
                headers=token
            )

        with allure.step("Проверка: статус 200 и совпадение номера заказа"):
            assert get_response.status_code == 200
            assert get_response.json()['orders'][0]['number'] == create_response.json()['order']['number']

    @allure.title('Ошибка при получении заказа неавторизованным пользователем')
    def test_get_order_user_without_authorisation_fail(self):
        with allure.step("Отправка запроса получения заказов без авторизации"):
            response = requests.get(APILinks.MAIN_URL + APILinks.ORDERS_URL)

        with allure.step("Проверка: статус 401 и сообщение об авторизации"):
            assert response.status_code == 401
            assert response.json()['message'] == "You should be authorised"
