from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          #sort_keys=True
        )
    ]
)


def test_post_v1_account():
    # Регистарция пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)
    login = 'tus_test37'
    password = '112233'
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)

    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'
    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()

    assert response.status_code == 200, 'Письма не были получены'
    # pprint.pprint(response.json())

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен "
    # user_token = token

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)

    assert response.status_code == 200, 'Пользователь не был активирован'
    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, 'Пользователь не смог авторизоваться'



def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            # print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token





