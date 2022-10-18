from dataclasses import dataclass
from logging import getLogger
from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel

log = getLogger("main")


@dataclass(frozen=True)
class Publication:
    """
    Publication is a class where the attributes of each
    of its objects are passed to the constructor.
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


class PublicationModel(BaseModel):
    id = 1016852
    authors = "Paula Kephart"
    isbn: Optional[List[str]] = ["1580173624", "9781580173629"]
    edition: Optional[str] = None
    series: Optional[str] = "A Storey country wisdom bulletin, A-270"
    title = "Housebound dogs: how to keep your stay-at-home dog happy & healthy"
    publisher: Optional[str] = "Storey Publishing, LLC"
    year = 2000
    pages = "32"
    lang = "English"
    size = "2 Mb"
    extension = "epub"
    mirrors: Dict[str, str] = {
        "libgen.io": "http://library.lol/main/708C30851BCF1D551335479CEEB1B90F",
        "libgen.pw": "http://libgen.lc/ads.php?md5=708C30851BCF1D551335479CEEB1B90F",
        "b-ok.org": "https://3lib.net/md5/708C30851BCF1D551335479CEEB1B90F",
        "bookfi.net": "https://library.bz/main/edit/708C30851BCF1D551335479CEEB1B90F",
    }


class MetaPublicationModel(BaseModel):
    search_url = "http://gen.lib.rus.ec/search.php"
    total_results: Optional[int] = 779
    page_result_range = "1-25/779"
    page = 1
    results: List[PublicationModel] = [PublicationModel()]


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
