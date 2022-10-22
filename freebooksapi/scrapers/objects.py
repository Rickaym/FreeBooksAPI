from dataclasses import dataclass
from enum import Enum
from logging import getLogger
from typing import Dict, List, Optional, Tuple

log = getLogger("main")


@dataclass(frozen=True)
class Publication:
    """
    A Publication, which includes all books, articles, magazines, comics,
    mangas and any sort of web-publications.
    """

    id: int
    authors: str
    isbn: str
    edition: str
    series: str
    title: str
    publisher: str
    year: int
    pages: str
    lang: str
    size: str
    extension: str
    mirrors: Dict[str, str]


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
    showing_range: Optional[Tuple[int, int]]

    def get_publications(self, offset: int, limit: int):
        pubs = self.publications[offset:]
        if len(pubs) > limit:
            return pubs[:limit]
        return pubs


@dataclass(frozen=True)
class LastAddedResult:
    publications: List[Publication]

    def get_publications(self, offset: int, limit: int):
        pubs = self.publications[offset:]
        if len(pubs) > limit:
            return pubs[:limit]
        return pubs
