---
sidebar_position: 1
---

# Overview

FreebooksAPI is written in Python using the [FastAPI](https://fastapi.tiangolo.com/)
toolchain for the API server and `bs4` & `lxml` for web scraping.

:::tip My tip

Although it is optimal,
you don't need to be aware of both the FastAPI toolchain and bs4. The API server
is completely independent to the scrapers except for interfaces.

:::


While it should be relatively simple to navigate through the files to understand their purposes, here is a quick guide:

- `main.py` - main infastructure like registering apis

- `models.py` - pydantic models used in automatic documentation
- `scrapers/` - the 'backend' for the API where the code for the scrapers live
- `scrapers/agent.py` - an abstract agent class
- `scrapers/ahttp.py` - simple async http wrapper
- `scrapers/libgen.py` - libgen agents
- `scrapers/zlibrary.py` - zlibrary agents
- `scrapers/objects.py` - object abstractions for passing around internally

# Setting up a development environment

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
