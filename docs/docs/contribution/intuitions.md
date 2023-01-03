---
sidebar_position: 2
---

# Intuitions

## Agents

Agents classes are intended for scraping the website (what to scrape will be mentioned later). They act as a layer of abstraction for our API Endpoint functions to call on.

In this example the User is accessing the Libgen API.

```
                 +......+
                 | User |
                 +------+
                    ^ | .- GET
   Responds JSON -. ^ |    http://127.0.0.1:8000/libgen/topics
          object    | v
            +-------------------+
            | /{library}/topics |
            +-------------------+
                    ^ | .- Calls GenLibRusEc.get_topics()
 Returns scraped -. ^ |
         objects    | v
            +--------------------+
            | GenLibRusEc(Agent) |
            +--------------------+
                    ^ |
 Returns WebPage -. ^ | .- GET Website
                    | v
           +------------------------+
           | http://gen.lib.rus.ec/ |
           +------------------------+
```

Having the Agent class as a layer of abstraction allows the API endpoint functions to depend on them wholly with a standardized interface regardless of the library it is calling upon.

I.e. libgen API uses the `GenLibRusEc` Agent, whereas libgenlc API uses `LibGenLc`, which are both subclasses of the `Agent` class, and so we're able to manage between different libraries in the same API endpoint.

```py
LIBRARY_AGENTS: Dict[str, Agent] = {
    Library.libgen: GenLibRusEc(),
    Library.libgenlc: LibGenLc(),
    ...
}

@FREEBOOKSAPI.get("/{library}/topics")
async def get_enlisted_topics(library: Library):
    return await LIBRARY_AGENTS[library].get_topics()
```

Each library agent determines the complete implementation of the interfacing methods such as `search()` `get_topics()` so long as they return the correct data in the object typed by the `Agent` class.

#### Disabling supporting certain Endpoints

If a specific library Agent is not able to support all methods specified by the `Agent` class, an extra step must be taken in removing the library as an acceptable `{library}` parameter in the API Endpoint declaration and leaving a `NotImplementedError` raised override of the method.

```py
# (some endpoint that doesn't support zlib)
@FREEBOOKSAPI.get("/{library}/example")
def get_last_added(library: LibraryLibgen):
    """
    Use `LibraryLibgen` for the Library parameter
    rather than `LibraryAll`.
    """
```

### Agent - Webserver independence

It is important that the Agent class does not depend on anything outside of itself as future releases of this API might ship them as an independent pypi project (there is also zero reason for the Agent class to depend outside the folder, if your contribution happen to need something of that sort, reconsider!)

This independence also means that if you're contributing an Agent for a library, although it would be optimal, you aren't necessatited to understand the FastAPI infastructure that interacts with the Agent classes.

### No Internal Caching

Also do refrain from carrying out caching inside the Agent classes as there will be a caching implementation directly on the Agent class intended in the future.

If you have any questions shoot me a DM or write on `#freebooksapi` :D
