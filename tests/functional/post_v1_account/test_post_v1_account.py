from datetime import datetime

import pytest
from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to
from pygments.lexers.graphics import PostScriptLexer

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account


def test_post_v1_account(
        account_helper,
        prepare_user
        ):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1Account.check_response_values(response)
    print(response)





@pytest.mark.parametrize('login, email, password',
                         [
                             ('6tus_444', '6tus_444@mail.ru', '12345'),
                             ('7tus_444', '7tus_444mail.ru', '1234567'),
                             ('8', '8tus_444@mail.ru', '1234567')
                         ])

def test_post_v1_account_neg( account_helper,login, email, password):
        with check_status_code_http(400, 'Validation failed'):
            account_helper.register_new_user(login=login, password=password, email=email)




