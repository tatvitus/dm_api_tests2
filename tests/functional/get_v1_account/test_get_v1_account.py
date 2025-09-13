from datetime import datetime

import requests
from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to,
    has_items,
)

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http

import allure

@allure.suite("Тесты на проверку метода GET v1/account")
@allure.sub_suite("Позитивные тесты")
@allure.title("Получение данных о пользователе")
def test_get_v1_account(auth_account_helper):
    response=auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
    GetV1Account.check_response_values_get_v1_account(response)
    print(response)

@allure.suite("Тесты на проверку метода GET v1/account")
@allure.sub_suite("Негативные тесты")
@allure.title("Ошибка получения данных, если пользователь не зарегистрирвоан")
def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
