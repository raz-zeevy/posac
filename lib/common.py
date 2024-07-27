from typing import Tuple


def parse_range_string(value: str) -> Tuple[int, int]:
    from_, to_ = value.split('-')
    return int(from_), int(to_)