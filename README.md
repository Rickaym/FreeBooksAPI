# FreeBooksAPI

A comprehensive (unofficial) API service for [gen.lib.rus.ec/libgen.rs](http://gen.lib.rus.ec/) , [libgen.lc/libgen.li](http://libgen.lc/), [Z-Library](http://b-ok.org/) and [libgen.me](http://libgen.me/) (essentially all the mirrors [here](https://forum.mhut.org/viewtopic.php?p=9000))

### Features
- Searching books by name, author name, topic and the likes.
- Performing a full text search for books
- Retrieving downloadable/torrent links for book

# Contribution

The underlying API server infastructure is written with [FastAPI](https://fastapi.tiangolo.com/) in Python. While it should be relatively simple to navigate through the files to understand their purposes, here is a quick guide:

- `main.py` - main infastructure like registering routes and so on
- `models.py` - pydantic models used in automatic documentation
- `scrapers/` - the 'backend' for the API where the code for the scrapers live

- `scrapers/agent.py` - an abstract agent class
- `scrapers/ahttp.py` - simple async http wrapper
- `scrapers/libgen.py` - libgen agents
- `scrapers/zlibrary.py` - zlibrary agents
- `scrapers/objects.py` - general classes for passing around internally


## Agents (intuition)

Agents classes are intended to be directly interacted for scraping the corresponding websites with the given task. Libgen agents, for instance, acts as an abstraction for the API Endpoints to call on, and thus methods such as `search()`, `get_topics()` must readily return the result object in a single call. The underlying implementation of how that is achieved is open up to the agent implementation, and thus we're able to collectively call these scrapers as long as they support the main methods specified by `agent.py`.

If a specific library agent cannot support all methods specified by the `Agent` abstract class, an extra step needs to be taken. If a specific library agent is unable to support the required method, you should remove the specific library as an acceptable `{library}` parameter and raising `NotImplementedError` after overriding the corresponding method.

`NOTE: the scrapers must not have any dependencies outside of them, and there are no reason to have so`

Future releases of this API might possibly ship the scrapers as an independent pypi project.


