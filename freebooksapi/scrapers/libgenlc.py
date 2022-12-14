from urllib.parse import urlencode
from traceback import print_exception
from typing import Any, Dict

from .genlibrusec import GenLibRusEc
from .agent import SearchResult
from .objects import Publication, SearchUrlArgs, Datadump
from .utilities import get_href


class LibGenLc(GenLibRusEc):
    def __init__(self) -> None:
        super().__init__(
            search_url="https://libgen.lc/index.php",
            datadumps_url="https://libgen.lc/dirlist.php?dir=dbdumps",
        )

    # The topics and topic ids of the parent library and this library is the same so do not change the topics_url
    def get_search_url(self, search_term: str, args: SearchUrlArgs) -> str:
        # Gmode is needed to get the acutal table inside the html instead of a dummy html
        urlargs = {"req": search_term, "page": args.page, "gmode": "on"}
        if args.limit in (25, 50, 100):
            urlargs["res"] = args.limit
        if args.topic_id:
            # Booktopicid can be combined with the name to be more specific
            search_term = (
                search_term + " " + f"booktopicid:{args.topic_id}"
                if search_term
                else f"booktopicid:{args.topic_id}"
            )
            urlargs["req"] = f"booktopicid:{args.topic_id}"
        if args.search_mode:
            # Fmode cannot be combined with name or booktopicid so get the lastest book only
            search_term = f"fmode:{args.search_mode.value}"
            urlargs["topics1"] = "all"
        urlargs["req"] = search_term
        return f"{self.search_url}?{urlencode(urlargs)}"

    def parse_result(self, page):
        tables = page.find_all("table")
        files_count = page.find_all("ul")[1].find("span")
        # If total_files is not there the amount of files is not known(usually occurs when getting last added files)
        total_files = files_count.text if files_count else "??"
        results = []
        if int(total_files) > 0:
            rows = tables[1].find_all("tr")
            for row in rows[1:]:
                cells = row.find_all("td")
                try:
                    attrs = self._extract_attributes(cells)
                except Exception as e:
                    print_exception(e.__class__, e, e.__traceback__)
                    continue
                results.append(Publication(**attrs))
        return SearchResult(results, int(total_files), (0, 0))

    def _extract_attributes(self, cells) -> Dict[str, Any]:
        attrs: Dict[str, Any] = {
            "edition": None,
            "series": None,
            "isbn": None,
            "lang": "N/A",
        }
        # This is the ideal type of row with all the informations
        offset = 0
        if len(cells) == 9:
            offset = 4
            edition_and_series_container = cells[0].find("b")
            if edition_and_series_container:
                edition_and_series_container = edition_and_series_container.find_all(
                    "a"
                )
                if len(edition_and_series_container) > 0:
                    attrs["series"] = edition_and_series_container[0].text.strip()
                if len(edition_and_series_container) > 1:
                    attrs["edition"] = edition_and_series_container[1].text.strip()
            t = cells[0].findChildren("a", recursive=False, limit=1)
            if t:
                t = t[0]
                attrs["title"] = t.text
                attrs["id"] = t.get("href").split("id=")[-1]
            else:
                attrs["title"] = ""
                # Replace with series id if no title
                attrs["id"] = (
                    edition_and_series_container[0].get("href").split("id=")[-1]
                )
            isbn = []
            # ISBN and other such informations are in green
            for el in cells[0].find_all("font"):
                if el.get("color") == "green":
                    isbn += [i.strip() for i in el.text.split(";")]
            attrs["isbn"] = isbn
            attrs["authors"] = cells[1].text.strip() or "N/A"
            attrs["publisher"] = cells[2].text or "N/A"
            # The year is always at the front so take the first 4 letters and convert to year
            attrs["year"] = int(cells[3].text[:4]) if cells[3].text else -1
            attrs["lang"] = cells[4].text or "N/A"
        # There is another type of row where there is only title,page,size,extension and mirror
        else:
            attrs["id"] = -1  # No id
            # Title can be in a span tag or in an a tag
            attrs["title"] = cells[0].find("a").text
            if attrs["title"] == "":
                attrs["title"] = cells[0].find("span").text
        attrs["pages"] = cells[1 + offset].text.split("/")[-1].strip()
        attrs["size"] = cells[2 + offset].text
        attrs["extension"] = cells[3 + offset].text
        attrs["mirrors"] = [
            link.get("href") for link in cells[4 + offset].find_all("a")
        ]
        return attrs

    def _extract_dbdumps_attrs(self, cell):
        columns = cell.find_all("td")
        if not columns:
            return {}
        return {
            "name": columns[0].text,
            "url": "https://libgen.lc/" + get_href(columns[0]),
            "last_modified": columns[2].text,
            "size": f"{round(int(columns[1].text)/(1024*1024),2)}Mb",
            "description": "",
        }

    def parse_datadumps(self, page):
        dumps = []
        for row in page.find_all("tr")[1:]:
            if row:
                attrs = self._extract_dbdumps_attrs(row)
                if attrs:
                    dumps.append(Datadump(**attrs))
        return dumps

    def get_aliases(self):
        return ["http://libgen.lc/", "http://libgen.gs/", "http://libgen.li/"]
