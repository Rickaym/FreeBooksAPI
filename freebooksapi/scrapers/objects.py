from dataclasses import dataclass
from enum import Enum
from logging import getLogger
from typing import Dict, List, Optional, Tuple, Union

log = getLogger("main")


@dataclass(frozen=True)
class Publication:
    """
    A Publication, which includes all books, articles, magazines, comics,
    mangas and any sort of web-publications.
    """

    id: Union[str, int]
    authors: Optional[str]
    isbn: Optional[List[str]]
    edition: Optional[str]
    series: Optional[str]
    title: str
    publisher: Optional[str]
    year: Optional[Union[int, str]]
    pages: str
    lang: str
    size: str
    extension: str
    mirrors: List[str]


class SearchMode(str, Enum):
    last = "last"


@dataclass(frozen=True)
class SearchUrlArgs:
    lang: Optional[str]
    page: int
    limit: int
    offset: int
    topic_id: Optional[int]
    search_mode: Optional[SearchMode]


@dataclass(frozen=True)
class SearchResult:
    publications: List[Publication]
    total_found: int
    showing_range: Tuple[int, int]

    def get_publications(self, offset: int, limit: int):
        pubs = self.publications[offset:]
        if len(pubs) > limit:
            return pubs[:limit]
        return pubs


@dataclass(frozen=True)
class Datadump:
    name: str
    url: str
    last_modified: str
    size: str
    description: str
