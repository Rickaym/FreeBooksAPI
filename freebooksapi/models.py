from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel


class LibraryZlib(str, Enum):
    zlibrary = "zlibrary"


class LibraryLibgen(str, Enum):
    libgen = "libgen"
    libgenlc = "libgenlc"


class LibraryAll(str, Enum):
    libgen = LibraryLibgen.libgen.value
    libgenlc = LibraryLibgen.libgenlc.value
    zlibrary = LibraryZlib.zlibrary.value


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
