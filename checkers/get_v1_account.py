from datetime import datetime

from hamcrest import (
    assert_that,
    all_of,
    has_property,
    starts_with,
    has_properties,
    instance_of,
    has_items,
    equal_to,
)


class GetV1Account:
    @classmethod
    def check_response_values_get_v1_account(cls, response):
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

                        }
                    )
                )

            )

        )