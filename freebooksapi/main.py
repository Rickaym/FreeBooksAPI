import logging
import aiohttp

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from os import getenv
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from logging import getLogger
from typing import Dict, List, Optional
from misc import cache_cascade, set_cache
from exceptions import ErrorJsonResponse
from models import MetaPublicationModel, LibraryAll, LibraryLibgen, MetaDatadumpModel
from fastapi_versioning import VersionedFastAPI

from scrapers.agent import Agent
from scrapers.planetebooks import PlanetEBooks
from scrapers.genlibrusec import GenLibRusEc
from scrapers.libgenlc import LibGenLc
from scrapers.objects import SearchUrlArgs, SearchMode

FREEBOOKSAPI = VersionedFastAPI(docs_url=None, redoc_url=None)
FREEBOOKSAPI.mount("/home", StaticFiles(directory="home"), name="home")


def custom_mount(parent: FastAPI, version_key: str):
    return FastAPI(version=version_key, docs_url=None, redoc_url="/api-reference")


FREEBOOKSAPI.new_versioned_mount = custom_mount
RUNNER_DISHOOK_URL: str = getenv("RUNNER_DISHOOK_URL")  # type: ignore

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


@FREEBOOKSAPI.get("/", response_class=RedirectResponse, include_in_schema=False)
def index():
    return RedirectResponse("/home")


@FREEBOOKSAPI.get("/home", response_class=FileResponse, include_in_schema=False)
def home_resp():
    return FileResponse("./home/index.html")


@FREEBOOKSAPI.get("/docs", response_class=RedirectResponse, include_in_schema=False)
def docs():
    return RedirectResponse("./latest/api-reference")


# /v1/ Routes Below


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


@FREEBOOKSAPI.get(
    "/{library}/datadumps", route_version=1, response_model=MetaDatadumpModel
)
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


@FREEBOOKSAPI.get("/{library}/topics", route_version=1, response_model=Dict[str, str])
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
    route_version=1,
    response_description="Library URL Aliases.",
    response_model=List[str],
)
def get_torrent_aliases(library: LibraryAll):
    """
    Retrieve existing aliases for the given libraries.
    """
    return LIBRARY_AGENTS[library.value].get_aliases()


@FREEBOOKSAPI.get(
    "/{library}/search",
    route_version=1,
    response_description="A list of publications for the given query.",
    response_model=MetaPublicationModel,
)
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


FREEBOOKSAPI.enable_latest()


def custom_openapi(router: FastAPI):
    def openapi():
        # cache the generated schema
        if router.openapi_schema:
            return router.openapi_schema

        # custom settings
        openapi_schema = get_openapi(
            title="API Reference",
            version=router.version,
            openapi_version=router.openapi_version,
            description=router.description,
            terms_of_service=router.terms_of_service,
            contact=router.contact,
            license_info=router.license_info,
            routes=router.routes,
            tags=router.openapi_tags,
            servers=router.servers,
        )
        # setting new logo to docs
        openapi_schema["info"]["x-logo"] = {
            "url": "https://raw.githubusercontent.com/Rickaym/FreeBooksAPI/master/assets/logo-large.png"
        }
        router.openapi_schema = openapi_schema

        return router.openapi_schema

    return openapi


for router in FREEBOOKSAPI.route_version_mounts.values():
    router.openapi = custom_openapi(router)

print(FREEBOOKSAPI.route_version_mounts)
