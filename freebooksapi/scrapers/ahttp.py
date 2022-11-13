import asyncio
from logging import getLogger

import aiohttp
from bs4 import BeautifulSoup as soup

logger = getLogger("http")

HEAD = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}
TIMEOUT = aiohttp.ClientTimeout(total=90, connect=0, sock_connect=60, sock_read=90)


class LoopError(Exception):
    def __init__(self, *a) -> None:
        pass


async def get(url, jar=None, proxy_list=None):
    try:
        async with aiohttp.ClientSession(
            headers=HEAD,
            cookie_jar=jar,
            timeout=TIMEOUT,
            connector=ChainProxyConnector.from_urls(proxy_list) if proxy_list else None,
        ) as sess:
            logger.info("GET %s" % url)
            async with sess.get(url) as resp:
                return await resp.text()
    except asyncio.exceptions.CancelledError:
        raise LoopError("Asyncio loop had been closed before request could finish.")


async def get_page(url, strain=None, proxy_list=[]):
    con = await get(url, proxy_list=proxy_list)
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(con)
    return soup(con, features="lxml", parse_only=strain)
