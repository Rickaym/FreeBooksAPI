from typing import Optional
from urllib.parse import urlencode, urlparse
from bs4 import SoupStrainer
from .objects import Publication, SearchResult, SearchUrlArgs
from .agent import Agent
from .ahttp import get_page
from .utilities import get_href


def suburl_soupstrainer(elem, attrs):
    if elem not in ["h6", "a"]:
        return False

    if elem == "a" and (attrs.get("class") is None or attrs["class"] != "buttonpe"):
        return False

    return True


class PlanetEBooks(Agent):
    suburl_soupstrain = SoupStrainer(suburl_soupstrainer)

    def __init__(
        self,
    ) -> None:
        super().__init__(
            search_url="https://www.planetebook.com/",
            topics_url="",
            datadumps_url="",
            search_strain=SoupStrainer("h2", {"class": "fusion-post-title"}),
        )

    def get_page_url(self, search_term: Optional[str], urlargs: SearchUrlArgs) -> str:
        # search_term can never be none for this library
        url = f"{self.search_url}?{urlencode({'s': search_term})}"
        return url

    def parse_topics(self, page):
        pass

    async def _follow_suburl(self, suburl: str, attrs: dict):
        page = await get_page(suburl, self.suburl_soupstrain)
        year = page.find("h6").text.split(",").pop().strip()
        attrs["year"] = int(year) if year.isnumeric() else year if year else None
        attrs["mirrors"] = [f"{self.search_url[:-1]}{url.get('href')}" for url in page.find_all("a", {"class": "buttonpe"}, href=True)]

    async def parse_result(self, page):
        covers = page.find_all("h2")
        found = len(covers)

        results = []
        for sample in covers:
            attrs = {}
            attrs["title"] = sample.text
            sub_url = get_href(sample)
            attrs["id"] = urlparse(sub_url).path.replace("/", "")
            await self._follow_suburl(sub_url, attrs)
            results.append(attrs)

        return SearchResult(
            [
                Publication(
                    authors="",
                    isbn=None,
                    edition=None,
                    series=None,
                    publisher=None,
                    pages="",
                    lang="",
                    size="",
                    extension="",
                    **res,
                )
                for res in results
            ],
            found,
            (found, found),
        )

    def parse_datadumps(self, page):
        raise NotImplementedError
