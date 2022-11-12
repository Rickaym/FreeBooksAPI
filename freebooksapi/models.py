from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class LibraryPlanetEBooks(str, Enum):
    planetebooks = "planetebooks"


class LibraryLibgen(str, Enum):
    libgen = "libgen"
    libgenlc = "libgenlc"


class LibraryAll(str, Enum):
    libgen = LibraryLibgen.libgen.value
    libgenlc = LibraryLibgen.libgenlc.value
    planetebooks = LibraryPlanetEBooks.planetebooks.value


class DatadumpModel(BaseModel):
    name = "fiction.rar"
    url = "https://libgen.is/dbdumps/fiction.rar"
    last_modified: str = "2022-10-24 04:37"
    size: str = "1.0G"
    description: str = (
        "Housebound dogs: how to keep your stay-at-home dog happy & healthy"
    )


class MetaDatadumpModel(BaseModel):
    datadump_url = "https://libgen.is/dbdumps/"
    total_results: int = 33
    results: List[DatadumpModel] = [DatadumpModel()]


class PublicationModel(BaseModel):
    id: Union[str, int] = 1016852
    authors: Optional[str] = "Paula Kephart"
    isbn: Optional[List[str]] = ["1580173624", "9781580173629"]
    edition: Optional[str] = None
    series: Optional[str] = "A Storey country wisdom bulletin, A-270"
    title = "Housebound dogs: how to keep your stay-at-home dog happy & healthy"
    publisher: Optional[str] = "Storey Publishing, LLC"
    year: Optional[Union[int, str]] = 2000
    pages = "32"
    lang = "English"
    size = "2 Mb"
    extension = "epub"
    mirrors: List[str] = [
        "http://library.lol/main/708C30851BCF1D551335479CEEB1B90F",
        "http://libgen.lc/ads.php?md5=708C30851BCF1D551335479CEEB1B90F",
        "https://3lib.net/md5/708C30851BCF1D551335479CEEB1B90F",
        "https://library.bz/main/edit/708C30851BCF1D551335479CEEB1B90F",
    ]


class MetaPublicationModel(BaseModel):
    search_url = "http://gen.lib.rus.ec/search.php"
    total_results: Optional[int] = 779
    page_result_range = "1-25/779"
    page = 1
    results: List[PublicationModel] = [PublicationModel()]
