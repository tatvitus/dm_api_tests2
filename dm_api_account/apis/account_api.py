import requests

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            registration: Registration
    ):
        """
        Register new user
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def get_v1_account(
            self,
            **kwargs
    ):
        """
        Get current user
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        return response

    def put_v1_account_token(
            self,
            token,
            validate_response=True
    ):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
            # **kwargs
    ):
        """
        Change registered user email
        :return:
        """
        response = self.put(
            path=f'/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True)
            # **kwargs
        )
        return response

    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            # **kwargs
    ):
        """
        Change registered user password
        """
        response = self.put(
            path=f'/v1/account/password',
            # **kwargs,
            json=change_password.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            **kwargs
    ):
        """
        Reset registered user password
        :param
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            **kwargs,
            json = reset_password.model_dump(exclude_none=True, by_alias=True)
        )
        return response

