# 🏗️ Contribution

To understand the server infastructure and scrapers you will have to understand the intuitions behind the components that ensures that FreeBooksAPI works like a well oiled machine.

You can skip this part if you're here just to view the API endpoint documentation.

## Index

1. [Overview](#overview)
2. [Setting up a development environment](#setting-up-a-development-environment)
3. [Intuitions](#intuitions)

   3.1. [Agents](#agents)

## Overview

The project is written completely in Python using the [FastAPI](https://fastapi.tiangolo.com/) toolchain for the API server and using `bs4` & `lxml` for web scraping.
Although it is optimal, you don't need to be aware of both the FastAPI toolchain and bs4 as they are completely independent to each other.

While it should be relatively simple to navigate through the files to understand their purposes, here is a quick guide:

- `main.py` - main infastructure like registering apis

- `models.py` - pydantic models used in automatic documentation
- `scrapers/` - the 'backend' for the API where the code for the scrapers live
- `scrapers/agent.py` - an abstract agent class
- `scrapers/ahttp.py` - simple async http wrapper
- `scrapers/libgen.py` - libgen agents
- `scrapers/zlibrary.py` - zlibrary agents
- `scrapers/objects.py` - object abstractions for passing around internally

## Setting up a development environment

To start working on the project you'll have to setup a development environment.
This guide assumes you have an installation of:

1. Python of version at least `3.9`
2. Git CLI

Follow these in order:

1. Open a Terminal or a Command Prompt in a directory you want to clone the repository into and use the following command :

```
git clone https://github.com/Rickaym/FreeBooksAPI
```

2. Install the required dependencies by running the following command:

```
# Linux/macOS
python3 -m pip install -r .\requirements.txt

# Windows
py -3 -m pip install -r .\requirements.txt
```

3. Change the working directory into `./freebooksapi` through the following command:

```
cd freebooksapi
```

4. If you've followed the steps correctly, you should be able to use the following command to start a ASGI server:

```
# Linux/macOS
uvicorn main:FREEBOOKSAPI --reload

# Windows
.\debug.bat
```

This will open an ASGI server on your localhost network at `http://127.0.0.1:8000`.

### Debugging API Endpoints

Once you've successfully started the uvicorn server, you'll be able to send requests to the API endpoints through sending the appropriate requests (GET/POST/PUT) to the endpoints. You can simply vising the endpoint on your web browser to simulate a GET request, but for other types of requests, you can use HTTP clients like Thunder Client or Rapid API Client.

#### Testing

We have the **GET** endpoint `/{library}/topics`. With our ASGI server opened at `http://127.0.0.1:8000` we'll need to send a **GET** request to `http://127.0.0.1:8000/{library}/topics` to test the endpoint.

Also, the syntax `{library}` is a parameter that the user has to substitute with a valid library name, e.g. `http://127.0.0.1:8000/libgen/topics`
returning an application/json response such as this

```json
{"Technology":210,"Aerospace Equipment":212,"Automation":211,
"Communication: Telecommunications":235,"Communication":234,
"Construction":236...}
```

## Intuitions

### Agents

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

#### Agent - Webserver independence

It is important that the Agent class does not depend on anything outside of itself as future releases of this API might ship them as an independent pypi project (there is also zero reason for the Agent class to depend outside the folder, if your contribution happen to need something of that sort, reconsider!)

This independence also means that if you're contributing an Agent for a library, although it would be optimal, you aren't necessatited to understand the FastAPI infastructure that interacts with the Agent classes.

#### No Internal Caching

Also do refrain from carrying out caching inside the Agent classes as there will be a caching implementation directly on the Agent class intended in the future.

If you have any questions shoot me a DM or write on `#freebooksapi` :D
