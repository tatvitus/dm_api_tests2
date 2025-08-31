from dm_api_account.models.login_credentials import LoginCredentials


def test_put_v1_account_email(account_helper, prepare_user,
                              account=None, remember_me=True):

    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)  #регистрация
    account_helper.user_login(login=login, password=password) #авторизация
    account_helper.change_email(login=login, password=password, email=email) #смена email
    # Пытаемся войти, получаем 403
    login_credentials = LoginCredentials(
        login=login,
        password=password,
        remember_me=remember_me
    )
    response = account_helper.dm_account_api.login_api.post_v1_account_login(login_credentials=login_credentials)
    assert response.status_code == 403, f'Получен другой код ответа {response.status_code}'

    # Получить письма
    # Получить новый активационный токен для подтверждения смены email
    token = account_helper.get_token(login=login, token_type="activation")
    assert token is not None, f"Токен для пользователя {login} не был получен "

    # Активация пользователя c новой почты
    account_helper.activate_user(token=token)

    # Авторизация пользователя с новой почты
    account_helper.user_login(login=login, password=password) #повторный вход

