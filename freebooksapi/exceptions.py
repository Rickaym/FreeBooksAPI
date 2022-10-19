class LoopError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NoDomainError(Exception):
    def __init__(self):
        super().__init__("No working domain found. Try another time.")


class EmptyQueryError(Exception):
    def __init__(self):
        super().__init__("Search query is empty.")


class ProxyNotMatchError(Exception):
    def __init__(self):
        super().__init__("proxy_list must be a list.")


class BadSearchTerm(Exception):
    pass


class NoResults(Exception):
    """Search didn't return any results."""

    def __init__(self) -> None:
        msg = "Search didn't return any results."
        Exception.__init__(self, msg)


class NoAvailableMirror(Exception):
    """No mirrors are available to process request."""

    def __init__(self) -> None:
        msg = "No mirrors are available to process the request at this time."
        Exception.__init__(self, msg)


class CouldntFindDownloadUrl(Exception):
    """MirrorDownloader couldn't extract the download URL."""

    def __init__(self, url: str) -> None:
        msg = f"Can't find the download URL in '{url}'"
        Exception.__init__(self, msg)
