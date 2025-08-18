from json import loads

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          #sort_keys=True
        )
    ]
)

def test_put_v1_account_email():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'tus4_test54'
    password = '112233'
    email = f'{login}@mail.ru'

    account_helper.register_new_user(login=login, password=password, email=email)  #регистрация
    account_helper.user_login(login=login, password=password) #авторизация

    # Меняем email
    json_data = {
        'login': login,
        'password': password,
        'email': email,
    }
    response = account.account_api.put_v1_account_email(json_data=json_data)
    assert response.status_code == 200, 'Пользователь не смог изменить емейл'

    # Пытаемся войти, получаем 403
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = account.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, f'Получен другой код ответа {response.status_code}'

    # Получить письма
    # Получить новый активационный токен для подтверждения смены email
    token = account_helper.get_activation_token_by_login(login=login)
    assert token is not None, f"Токен для пользователя {login} не был получен "

    # Активация пользователя c новой почты
    response = account.account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, 'Пользователь не был активирован'

    # Авторизация пользователя с новой почты
    account_helper.user_login(login=login, password=password) #повторный вход

