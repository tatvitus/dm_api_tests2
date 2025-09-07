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

from checkers.http_checkers import check_status_code_http


def test_get_v1_account(auth_account_helper):
    response=auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
    assert_that(
        response, all_of(
            has_property(
                'resource', has_properties(
                    {
                        'login': starts_with("tus"),
                        'online': instance_of(datetime),
                        'roles': has_items("Guest", "Player"),
                        'registration': instance_of(datetime),
                        'rating': has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                        # 'settings': has_properties(
                        #     {
                        #         "colorSchema": equal_to("Modern"),
                        #         "paging": has_properties(
                        #             {
                        #                 "postsPerPage": equal_to(10),
                        #                 "commentsPerPage": equal_to(10),
                        #                 #"topicsPerPage": equal_to(10),
                        #                 "messagesPerPage": equal_to(10),
                        #                 "entitiesPerPage": equal_to(10)
                        #             }
                        #         )
                        #
                        #     }




                    }
                )
            )

        )

    )
    print(response)


def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
