import logging
from logging import getLogger
from typing import Dict, Optional
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import MetaPublicationModel
from scrapers.agent import Agent
from scrapers.genlibrusec import GenLibRusEc
from scrapers.libgenlc import LibGenLc
from scrapers.objects import SearchUrlArgs
from models import LibraryAll

FREEBOOKSAPI = FastAPI()

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

CURRENT_VERSION = "v1"
VERSIONS = [CURRENT_VERSION]


class ErrorJsonResponse(JSONResponse):
    def __init__(self, status_code: int, status_name: str, message: str) -> None:
        super().__init__(
            jsonable_encoder(
                {
                    "error": {
                        "code": status_code,
                        "message": message,
                        "status": status_name,
                    }
                }
            ),
            status_code=status_code,
        )


@FREEBOOKSAPI.on_event("startup")
async def startup_event():
    pass


@FREEBOOKSAPI.get(
    "/{library}/topics",
)
async def get_enlisted_topics(library: LibraryAll):
    """
    Retrieve available topics for the library. The topic IDs fetched here can
    be used in the `/search` endpoint via `topic_id`.
    """
    return await LIBRARY_AGENTS[library].get_topics()


@FREEBOOKSAPI.get(
    "/{library}/last-added",
)
def get_last_added(library: LibraryAll):
    """
    Retrieve most recently added publications.
    """
    pass


@FREEBOOKSAPI.get(
    "/{library}/aliases",
    response_description="Library URL Aliases.",
)
def get_aliases(library: LibraryAll):
    """
    Retrieve existing aliases for the given libraries.
    """
    if (library.value == LibraryAll.libgen.value):
      return ["http://libgen.rs/", "http://libgen.is/", "http://libgen.st/"]
    elif (library.value == LibraryAll.libgenlc.value):
      return ['http://libgen.lc/', 'http://libgen.gs/', 'http://libgen.li/']


@FREEBOOKSAPI.get(
    "/{library}/search",
    response_description="A list of publications for the given query.",
    response_model=MetaPublicationModel,
)
def get_publications(
    library: LibraryAll,
    query: str,
    topic_id: Optional[int] = None,
    limit: int = 25,
    offset: int = 0,
    lang: Optional[str] = None,
    page: int = 1,
):
    """
    Retrieve all publications under a query.

    To get all publications under a specific topic, you can specify the query
    as `'*'` with a valid topic id.
    """
    if query == "*" and topic_id is None:
        return ErrorJsonResponse(
            404, "BADARGUMENT", f"You cannot use the '*' query without a topic id."
        )

    agent = LIBRARY_AGENTS[library.value]
    result = agent.query(
        query,
        SearchUrlArgs(
            lang=lang, page=page, topic_id=topic_id, limit=limit, offset=offset
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
