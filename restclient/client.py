from requests import (
    session,
    JSONDecodeError,
)
import structlog
import uuid
import curlify
from swagger_coverage_py.listener import CoverageListener
from swagger_coverage_py.request_schema_handler import RequestSchemaHandler
from swagger_coverage_py.uri import URI

from restclient.configuration import Configuration
from restclient.utilities import allure_attach


class RestClient:
    def __init__(
            self,
            configuration: Configuration
    ):
        self.host = configuration.host
        self.set_headers(configuration.headers)
        self.disable_log = configuration.disable_log
        self.session = session()
        self.log = structlog.get_logger(__name__).bind(service='api')

    # @allure_attach
    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    #@allure_attach
    def post(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='POST', path=path, **kwargs)

    #@allure_attach
    def get(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='GET', path=path, **kwargs)

    #@allure_attach
    def put(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='PUT', path=path, **kwargs)

    #@allure_attach
    def delete(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='DELETE', path=path, **kwargs)

    @allure_attach
    def _send_request(
            self,
            method,
            path,
            **kwargs
    ):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url = self.host + path

        if self.disable_log:
            rest_response = self.session.request(method=method, url=full_url, **kwargs)
            rest_response.raise_for_status()
            return rest_response

        log.msg(
            event='Request',
            method=method,
            full_url=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get('headers'),
            json=kwargs.get('json'),
            data=kwargs.get('data')
        )
        rest_response = self.session.request(method=method, url=full_url, **kwargs)
        curl = curlify.to_curl(rest_response.request)

        uri = URI(host=self.host, base_path="", unformatted_path=path, uri_params=kwargs.get('params'))
        RequestSchemaHandler(
            uri, method.lower(), rest_response, kwargs
        ).write_schema()

        print(curl)

        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            json=self._get_json(rest_response),
        )
        rest_response.raise_for_status()
        return rest_response

    @staticmethod
    def _get_json(
            rest_response
            ):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
