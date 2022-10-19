import re
from logging import getLogger
from traceback import print_exception
from typing import Any, Dict
from urllib.parse import urlencode

from .agent import Agent, SearchResult
from .objects import Publication, SearchUrlArgs
from .utilities import get_href

log = getLogger("libgen")

RE_ISBN = re.compile(
    r"(ISBN[-]*(1[03])*[ ]*(: ){0,1})*" + r"(([0-9Xx][- ]*){13}|([0-9Xx][- ]*){10})"
)

RE_EDITION = re.compile(r"(\[[0-9] ed\.\])")
RE_SEARCH_INFO = re.compile(
    r"(\d*) files found(?: \| showing results from (\d*) to (\d*))?"
)
RE_TOPIC_HREF = re.compile(r"topicid(\d*)")


class GenLibRusEc(Agent):
    def __init__(self) -> None:
        super().__init__(
            search_url="http://gen.lib.rus.ec/search.php",
            topics_url="http://gen.lib.rus.ec/",
        )

    def get_page_url(self, search_term: str, args: SearchUrlArgs) -> str:
        urlargs = {"req": search_term, "page": args.page}

        if args.limit in (25, 50, 100):
            urlargs["res"] = args.limit
        if args.topic_id:
            urlargs["req"] = f"topicid{args.topic_id}"

        return f"{self.search_url}?{urlencode(urlargs)}"

    def parse_topics(self, page):
        column = page.find("div", {"class": "dropdown_5columns align_right"})
        hrefs = column.find_all("a")
        return {
            a.text: int(RE_TOPIC_HREF.search(a.get("href")).groups()[0]) for a in hrefs
        }

    def parse_result(self, page):
        tables = page.find_all("table")

        rows = tables[2].find_all("tr")
        results = []
        for row in rows[1:]:
            cells = row.find_all("td")
            try:
                attrs = self._extract_attributes(cells)
            except Exception as e:
                print_exception(e.__class__, e, e.__traceback__)
                continue
            results.append(Publication(**attrs))

        meta_tags = tables[1].find_all("td")

        meta_inf = RE_SEARCH_INFO.search(meta_tags[0].text)
        if not meta_inf:
            total_files = 0
            show_range = None
        else:
            total_files = int(meta_inf.groups()[0])
            show_range = (
                (
                    int(meta_inf.groups()[1]),
                    int(meta_inf.groups()[2]),
                )
                if meta_inf.groups()[1] is not None
                else (1, len(results))
            )

        return SearchResult(results, total_files, show_range)

    def _extract_attributes(self, cells) -> Dict[str, Any]:
        attrs: Dict[str, Any] = {"edition": None, "series": None, "isbn": None}
        attrs["id"] = int(cells[0].text)
        attrs["authors"] = cells[1].text.strip() or None

        # The 2nd cell contains title information
        # In best case it will have: Series - Title - Edition - ISBN
        # But everything except the title is optional
        # and this optional text shows up in green font
        for el in cells[2].find_all("font"):
            et = el.text
            if RE_ISBN.search(et) is not None:
                # A list of ISBNs
                attrs["isbn"] = [
                    RE_ISBN.search(N).group(0)  # type: ignore
                    for N in et.split(",")
                    if RE_ISBN.search(N) is not None
                ]
            elif RE_EDITION.search(et) is not None:
                attrs["edition"] = et
            else:
                attrs["series"] = et

            # Remove this element from the DOM
            # so that it isn't considered a part of the title
            el.extract()

        # Worst case: just fill everything in the title field
        attrs["title"] = cells[2].text.strip()

        attrs["publisher"] = cells[3].text or None
        attrs["year"] = int(cells[4].text) or None
        attrs["pages"] = cells[5].text
        attrs["lang"] = cells[6].text
        attrs["size"] = cells[7].text
        attrs["extension"] = cells[8].text

        libgen_io_url = get_href(cells[9])
        libgen_pw_url = get_href(cells[10])
        bok_org_url = get_href(cells[11])
        bookfi_net_url = get_href(cells[12])

        # TODO: each of these _url can be None
        attrs["mirrors"] = {
            "libgen.io": libgen_io_url,
            "libgen.pw": libgen_pw_url,
            "b-ok.org": bok_org_url,
            "bookfi.net": bookfi_net_url,
        }
        return attrs


