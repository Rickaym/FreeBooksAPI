"""Utilities module.

Contains useful functions that don't belong to any class in particular.
"""
from typing import Any, Optional

from bs4 import Tag


def get_href(cell: Tag) -> Optional[str]:
    links = cell.find_all("a", href=True)
    first = next(iter(links), None)
    return None if first is None else first.get("href")

def try_int(obj: Any):
    if str(obj).isnumeric():
        return int(str(obj))
    return obj
