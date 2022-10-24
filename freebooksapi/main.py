import logging
from pkgutil import get_data

from fastapi import FastAPI
from logging import getLogger
from typing import Callable, Dict, List, Optional
from misc import cache_cascade, set_cache
from exceptions import ErrorJsonResponse
from models import MetaPublicationModel, LibraryAll, LibraryZlib, MetaDatadumpModel
from scrapers.agent import Agent
from scrapers.genlibrusec import GenLibRusEc
from scrapers.libgenlc import LibGenLc
from scrapers.objects import SearchUrlArgs, SearchMode

FREEBOOKSAPI = FastAPI(
    title="FreeBooksAPI",
    description="A comprehensive (unofficial) API service for gen.lib.rus.ec , libgen.lc, Z-Library and libgen.me.",
)

##### Logging
_loggers = ["main", "libgen", "zlibrary"]

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
stdout = logging.StreamHandler()
stdout.setFormatter(logFormatter)

for _logger in _loggers:
    _log_obj = logging.getLogger(_logger)
    _log_obj.setLevel(logging.DEBUG)
    _log_obj.addHandler(stdout)
log = getLogger("main")
##### Logging


LIBRARY_AGENTS: Dict[str, Agent] = {
    LibraryAll.libgen.value: GenLibRusEc(),
    LibraryAll.libgenlc.value: LibGenLc(),
}


@FREEBOOKSAPI.get("/{library}/search-fulltext", response_model=MetaPublicationModel)
async def get_publications_fulltext(library: LibraryZlib):
    """
    Perform a full text search to retrieve a publication.
    (only available on z-library)
    """
    raise NotImplementedError


async def cache_get_datadumps(cache_id: str):
    log.info(f'Retrieving cache information under "{cache_id}"')
    for name, lib in LIBRARY_AGENTS.items():
        canonical_name = cache_id.format(library=name)
        dbdumps = await lib.get_datadumps()
        log.info(f'Filled cache  "{canonical_name}" with "{len(dbdumps or [])}" items.')
        set_cache(canonical_name, dbdumps)


@FREEBOOKSAPI.get("/{library}/datadumps", response_model=MetaDatadumpModel)
@cache_cascade(
    cache_id="{library}/datadumps",
    cache_every_h=24,
    release_after_h=48,
    caching_task=cache_get_datadumps,
    pass_result=True,
)
def get_datadumps(library: LibraryAll):
    # `get_cached` attribute is set by the decorator
    dbdumps = get_datadumps.get_cached(library)
    return {
        "datadump_url": LIBRARY_AGENTS[library.value].datadumps_url,
        "total_results": len(dbdumps),
        "results": (item.__dict__ for item in dbdumps),
    }


async def cache_get_enlisted_topics(cache_id: str):
    log.info(f'Retrieving cache information under "{cache_id}"')
    for name, lib in LIBRARY_AGENTS.items():
        canonical_name = cache_id.format(library=name)
        topics = await lib.get_topics()
        log.info(f'Filled cache  "{canonical_name}" with "{len(topics or [])}" items.')
        set_cache(canonical_name, topics)


@FREEBOOKSAPI.get("/{library}/topics", response_model=Dict[str, str])
@cache_cascade(
    cache_id="{library}/topics",
    cache_every_h=24,
    release_after_h=48,
    caching_task=cache_get_enlisted_topics,
    pass_result=False,
)
async def get_enlisted_topics(library: LibraryAll):
    """
    Retrieve available topics for the library. The topic IDs fetched here can
    be used in the `/search` endpoint via `topic_id`.
    """
    # the data response needed for this endpoint is fetched from cache


@FREEBOOKSAPI.get(
    "/{library}/aliases",
    response_description="Library URL Aliases.",
    response_model=List[str],
)
def get_aliases(library: LibraryAll):
    """
    Retrieve existing aliases for the given libraries.
    """
    if library is LibraryAll.libgen:
        return ["http://libgen.rs/", "http://libgen.is/", "http://libgen.st/"]
    elif library is LibraryAll.libgenlc:
        return ["http://libgen.lc/", "http://libgen.gs/", "http://libgen.li/"]


@FREEBOOKSAPI.get(
    "/{library}/search",
    response_description="A list of publications for the given query.",
    response_model=MetaPublicationModel,
)
async def get_publications(
    library: LibraryAll,
    query: Optional[str] = None,
    topic_id: Optional[int] = None,
    limit: int = 25,
    offset: int = 0,
    lang: Optional[str] = None,
    page: int = 1,
    search_mode: Optional[SearchMode] = None,
):
    """
    Retrieve all publications under a query.

    To get all publications under a specific topic, you can specify a valid topic id.
    To get all latest publications, specify search_mode as last.
    """
    if query is None and (topic_id is None or search_mode is None):
        return ErrorJsonResponse(
            404,
            "BADARGUMENT",
            f"You cannot use leave the query empty without a topic id or a search mode.",
        )

    agent = LIBRARY_AGENTS[library.value]
    result = await agent.query(
        query,
        SearchUrlArgs(
            lang=lang,
            page=page,
            topic_id=topic_id,
            limit=limit,
            offset=offset,
            search_mode=search_mode,
        ),
    )
    if not result:
        return ErrorJsonResponse(
            404, "NOTFOUND", f"No publications founder under '{query}'."
        )

    if offset > len(result.publications):
        return ErrorJsonResponse(
            404,
            "BADARGUMENT",
            f"Cannot offset by {offset} with {len(result.publications)} results.",
        )

    return {
        "search_url": agent.search_url,
        "total_results": result.total_found if result.total_found is not None else None,
        "page_result_range": f"{result.showing_range[0]}-{result.showing_range[1]}/{result.total_found}"
        if result.showing_range is not None
        else None,
        "page": page,
        "results": (item.__dict__ for item in result.get_publications(offset, limit)),
    }
