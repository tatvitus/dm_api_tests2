import requests


def test_post_v1_account():
    # Регистарция пользователя


    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }
    login = 'tus_test'
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
    # Получить письма из почтового сервера
    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params)

    print(response.status_code)
    print(response.text)
    # Получить активационный токен
    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://5.63.153.31:5051/v1/account/b030e590-39c2-43ea-b6d6-268d129517bf', headers=headers)

    print(response.status_code)
    print(response.text)
    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
