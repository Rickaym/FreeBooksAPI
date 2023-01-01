import logging
import aiohttp

from fastapi import FastAPI
from os import getenv, path as file_path
from fastapi.responses import RedirectResponse
from logging import getLogger
from typing import Dict, List, Optional
from misc import cache_cascade, set_cache
from exceptions import ErrorJsonResponse
from models import MetaPublicationModel, LibraryAll, LibraryLibgen, MetaDatadumpModel
from fastapi_versioning import VersionedFastAPI, version, unversion

from scrapers.agent import Agent
from scrapers.planetebooks import PlanetEBooks
from scrapers.genlibrusec import GenLibRusEc
from scrapers.libgenlc import LibGenLc
from scrapers.objects import SearchUrlArgs, SearchMode

def get_description():
    readme = "README.md" if file_path.exists("README.md") else  "../README.md"

    with open(readme, 'r', encoding="utf-8") as file:
        content = file.read()

    content = content.replace("# FreeBooksAPI 🏛️", "# 🏛️ Introduction")

    contributions = "contributions.md" if file_path.exists("contributions.md") else "../contributions.md"
    with open(contributions, 'r', encoding="utf-8") as file:
        content += file.read()

    content = content.replace("[contributions.md](./contributions.md)", "[contribution](./#section/Contributions)")

    return content

FREEBOOKSAPI = FastAPI(
    title="FreeBooksAPI",
    description=get_description(),

)
RUNNER_DISHOOK_URL: str = getenv("RUNNER_DISHOOK_URL")  # type: ignore

with open("./index.html", "r") as f:
    INDEX_HTML = f.read()

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
    LibraryAll.planetebooks.value: PlanetEBooks(),
}

PERMITTED_FIELDS = "id,authors,isbn,edition,series,title,publisher,year,pages,lang,size,extension,mirrors"


@FREEBOOKSAPI.on_event("startup")
async def startup_event():
    if RUNNER_DISHOOK_URL is not None:
        async with aiohttp.ClientSession() as session:
            await session.post(
                RUNNER_DISHOOK_URL,
                data={
                    "content": "🚀 Heyall <#1032297422975680512> has been redeployed 💦"
                },
            )


@FREEBOOKSAPI.on_event("shutdown")
async def shutdown_event():
    if RUNNER_DISHOOK_URL is not None:
        async with aiohttp.ClientSession() as session:
            await session.post(
                RUNNER_DISHOOK_URL,
                data={
                    "content": "‼️ Heyall <#1032297422975680512> has been shut down 🛑"
                },
            )


async def cache_get_torrent_datadumps(cache_id: str):
    log.info(f'Retrieving cache information under "{cache_id}"')
    for name, lib in LIBRARY_AGENTS.items():
        canonical_name = cache_id.format(library=name)
        dbdumps = await lib.get_datadumps()

        dumps = {
            "datadump_url": LIBRARY_AGENTS[name].datadumps_url,
            "total_results": len(dbdumps),
            "results": [item.__dict__ for item in dbdumps],
        }

        log.info(f'Filled cache  "{canonical_name}" with "{len(dumps or [])}" items.')
        set_cache(canonical_name, dumps)


@FREEBOOKSAPI.get("/", response_class=RedirectResponse, include_in_schema=False)
@unversion()
def index():
    return RedirectResponse(
        "https://github.com/Rickaym/FreeBooksAPI/blob/master/README.md"
    )


@FREEBOOKSAPI.get("/{library}/datadumps", response_model=MetaDatadumpModel)
@version(1)
@cache_cascade(
    cache_id="{library}/datadumps",
    cache_every_h=24,
    stop_cache_after_h=48,
    caching_task=cache_get_torrent_datadumps,
)
def get_torrent_datadumps(library: LibraryAll):
    """
    Retrieve all datadump URLs.
    """
    # the response needed comes directly from cache


async def cache_get_topics(cache_id: str):
    log.info(f'Retrieving cache information under "{cache_id}"')
    for name, lib in LIBRARY_AGENTS.items():
        canonical_name = cache_id.format(library=name)
        topics = await lib.get_topics()
        log.info(f'Filled cache  "{canonical_name}" with "{len(topics or [])}" items.')
        set_cache(canonical_name, topics)


@FREEBOOKSAPI.get("/{library}/topics", response_model=Dict[str, str])
@version(1)
@cache_cascade(
    cache_id="{library}/topics",
    cache_every_h=24,
    stop_cache_after_h=48,
    caching_task=cache_get_topics,
)
async def get_topics(library: LibraryLibgen):
    """
    Retrieve available topics for the library. The topic IDs fetched here can
    be used in the `/search` endpoint via `topic_id`.
    """
    # the response needed comes directly from cache


@FREEBOOKSAPI.get(
    "/{library}/aliases",
    response_description="Library URL Aliases.",
    response_model=List[str],
)
@version(1)
def get_torrent_aliases(library: LibraryAll):
    """
    Retrieve existing aliases for the given libraries.
    """
    return LIBRARY_AGENTS[library.value].get_aliases()


@FREEBOOKSAPI.get(
    "/{library}/search",
    response_description="A list of publications for the given query.",
    response_model=MetaPublicationModel,
)
@version(1)
async def get_book_or_articles(
    library: LibraryAll,
    q: Optional[str] = None,
    topic_id: Optional[int] = None,
    limit: int = 25,
    offset: int = 0,
    lang: Optional[str] = None,
    page: int = 1,
    search_mode: Optional[SearchMode] = None,
):
    """
    Retrieve all book, article, and magazine publications through a query.

    To get publications under a specific topic, you can specify a valid topic id.
    To get all latest publications, specify search_mode as last.
    """
    if q is None and (topic_id is None or search_mode is None):
        return ErrorJsonResponse(
            404,
            "BADARGUMENT",
            f"You cannot use leave the query empty without a topic id or a search mode.",
        )

    agent = LIBRARY_AGENTS[library.value]
    result = await agent.search(
        q,
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
        return ErrorJsonResponse(404, "NOTFOUND", f"No publications found under '{q}'.")

    if offset > len(result.publications):
        return ErrorJsonResponse(
            404,
            "BADARGUMENT",
            f"Cannot offset by {offset} with {len(result.publications)} results.",
        )

    return {
        "search_url": agent.search_url,
        "total_results": result.total_found if result.total_found is not None else None,
        "page_result_range": f"{result.showing_range[0]}-{result.showing_range[1]}/{result.total_found}",
        "page": page,
        "results": (item.__dict__ for item in result.get_publications(offset, limit)),
    }


FREEBOOKSAPI = VersionedFastAPI(
    FREEBOOKSAPI,
    version_format="{major}",
    prefix_format="/v{major}",
    enable_latest=True,
)
