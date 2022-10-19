from dataclasses import dataclass
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


@dataclass(frozen=True)
class SearchUrlArgs:
    lang: Optional[str]
    page: int
    limit: int
    offset: int
    topic_id: Optional[int]


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
