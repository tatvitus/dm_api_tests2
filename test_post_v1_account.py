import json
import pprint

import requests
from json import loads


def test_post_v1_account():
    # Регистарция пользователя

    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }
    login = 'tus_test9'
    password = '112233'
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', headers=headers, json=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'
    # Получить письма из почтового сервера
    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Письма не были получены'
    # pprint.pprint(response.json())

    # Получить активационный токен
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            # print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    assert token is not None, f"Токен для пользователя {login} не был получен "
    # user_token = token

    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}', headers=headers)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Пользователь не был активирован'
    # # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Пользователь не смог авторизоваться'
