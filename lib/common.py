import itertools
from typing import Tuple


def parse_range_string(value: str) -> Tuple[int, int]:
    from_, to_ = value.split('-')
    return int(from_), int(to_)


def parse_indices_string(indices_string: str) -> set:
    if isinstance(indices_string, int):
        indices_string = str(indices_string)
    if not indices_string:
        return set()
    try:
        parsed_indices = indices_string.strip().split(",")
        parsed_indices = [x.strip() for x in parsed_indices]
        parsed_indices = [x.split("-") if "-" in x else x for x in parsed_indices]
        parsed_indices = [
            list(range(int(x[0]), int(x[1]) + 1)) if type(x) is list else [int(x)]
            for x in parsed_indices
        ]
        parsed_indices = set(itertools.chain(*parsed_indices))
        return parsed_indices
    except Exception as e:
        raise ValueError(f"Invalid indices string: {indices_string}, error: {e}")