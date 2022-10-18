import abc
from abc import ABC
from logging import getLogger

import requests
from bs4 import BeautifulSoup

from .ahttp import get_page
from .objects import SearchResult, SearchUrlArgs

NoResults = None
log = getLogger("agent")


class Agent(ABC):
    def __init__(self, search_url: str, topics_url: str) -> None:
        self.search_url = search_url
        self.topics_url = topics_url

    def query(
        self,
        search_term: str,
        urlargs: SearchUrlArgs
    ):
        """
        Returns result pages for a given search term.

        :param page_index: results page to start at
        :returns: BeautifulSoup4 object representing a result page
        """
        if search_term != "*" and len(search_term) < 3:
            raise ValueError("Your search term must be at least 3 characters long.")

        log.info(f"Searching for: '{search_term}'")

        page_url = self.get_page_url(search_term, urlargs)
        r = requests.get(page_url)

        if r.status_code == 200:
            with open("test.html", "w", encoding="utf-8") as f:
                f.write(r.text)
            result = self.parse_result(BeautifulSoup(r.text, "lxml"))

            if not result:
                raise NoResults
            else:
                return result

    async def get_topics(self):
        return self.parse_topics(await get_page(self.topics_url))

    @abc.abstractmethod
    def parse_topics(self, page: BeautifulSoup):
        raise NotImplementedError

    @abc.abstractmethod
    def get_page_url(self, search_term: str, urlargs: SearchUrlArgs) -> str:
        """Yields the new results page."""
        raise NotImplementedError

    @abc.abstractmethod
    def parse_result(self, page: BeautifulSoup) -> SearchResult:
        """Extract all the results info in a given result page.

        :param page: result page as an BeautifulSoup4 object
        :returns: list of :class:`Publication` objects
        """
        raise NotImplementedError
