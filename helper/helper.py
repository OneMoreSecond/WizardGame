__all__ = [
    'value_check'
]


def value_check(assertion, error_msg):
    if not assertion:
        raise error_msg
