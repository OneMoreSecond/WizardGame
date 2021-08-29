__all__ = [
    'value_check',
    'print_separator',
]


def value_check(assertion, error_msg):
    if not assertion:
        raise ValueError(error_msg)


def print_separator():
    print('-' * 20)
