import abc
from abc import ABC
from logging import getLogger
from typing import Any, Dict, List, Optional
from asyncio import iscoroutinefunction

from bs4 import BeautifulSoup, SoupStrainer

from .ahttp import get_page
from .objects import Datadump, SearchResult, SearchUrlArgs

log = getLogger("agent")


class Agent(ABC):
    """
    Retrieves HTML content from the corresponding library URLs for common
    operations like searching a book and parses out the data into Python objects.
    """

    def __init__(
        self,
        search_url: str,
        topics_url: str,
        datadumps_url: str,
        *,
        search_strain: Optional[SoupStrainer] = None,
        topics_strain: Optional[SoupStrainer] = None,
        datadumps_strain: Optional[SoupStrainer] = None
    ) -> None:
        self.search_url = search_url
        self.topics_url = topics_url
        self.datadumps_url = datadumps_url
        self.search_strain = search_strain
        self.topics_strain = topics_strain
        self.datadumps_strain = datadumps_strain

    async def query(self, search_term: Optional[str], urlargs: SearchUrlArgs):
        """
        Queries the search term along with the url args
        on the corresponding website.

        :param search_term: text query
        :param urlargs: other url arguments

        :returns: :class:`SearchResult`
        """
        if search_term and len(search_term) < 3:
            raise ValueError("Your search term must be at least 3 characters long.")

        page_url = self.get_search_url(search_term, urlargs)
        page = await get_page(page_url, self.search_strain)
        return (
            await self.parse_result(page)
            if iscoroutinefunction(self.parse_result)
            else self.parse_result(page)
        )

    def get_aliases(self):
        """
        Returns a set of aliases for the library.

        :returns: List[str]
        """
        raise NotImplementedError

    async def get_topics(self):
        if not self.topics_url:
            raise NotImplementedError
        return self.parse_topics(await get_page(self.topics_url, self.topics_strain))

    async def get_datadumps(self):
        if not self.datadumps_url:
            raise NotImplementedError
        return self.parse_datadumps(
            await get_page(self.datadumps_url, self.datadumps_strain)
        )

    @abc.abstractmethod
    def get_search_url(self, search_term: Optional[str], urlargs: SearchUrlArgs) -> str:
        """
        Encode all args into the search URL.

        :param search_term: text query
        :param urlargs: other url arguments

        :returns: args encoded URL string
        """
        raise NotImplementedError

    @abc.abstractmethod
    def parse_topics(self, page: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract all enlisted topics on the library.

        :param page: result page as an BeautifulSoup4 object
        :returns: Dict[str, Any] a mapping of topic name to topic ID
        """
        raise NotImplementedError

    @abc.abstractmethod
    def parse_result(self, page: BeautifulSoup) -> SearchResult:
        """
        Extract all publications and metadata in a given result page.

        :param page: result page as an BeautifulSoup4 object
        :returns: :class:`SearchResult`
        """
        raise NotImplementedError

    @abc.abstractmethod
    def parse_datadumps(self, page: BeautifulSoup) -> List[Datadump]:
        """
        Extract all external datadump links.

        :param page: result page as an BeautifulSoup4 object
        :returns: :class:`LastAddedResult`
        """
        raise NotImplementedError
