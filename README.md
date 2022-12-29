<div style="text-align: center">

# FreeBooksAPI 🏛️

<a href="https://freebooksapi.pyaesonemyo.me/latest/docs"><img alt="Extension Homepage" src="https://img.shields.io/badge/swagger-Docs-brightgreen?style=for-the-badge&logo=Swagger
"></a>
<a href="https://freebooksapi.pyaesonemyo.me/latest/redoc"><img alt="Extension Homepage" src="https://img.shields.io/badge/Redoc-docs-purple?style=for-the-badge&logo=Read the Docs"></a>


</div>

A comprehensive (unofficial) API service for [planet-ebooks](https://www.planetebook.com/), [gen.lib.rus.ec/libgen.rs](http://gen.lib.rus.ec/), [libgen.lc/libgen.li](http://libgen.lc/), providing access to retrieving free book downloading URLs, publication metadata, and many more!

## Features

- Searching books by name, author name, topic and etc...
- Retrieve free download URLs for books and publications
- Retrieve torrent datadumps for free books

## Quickstart

For API Reference, look at [Swagger Docs](https://freebooksapi.pyaesonemyo.me/latest/docs) or [ReDoc](https://freebooksapi.pyaesonemyo.me/latest/redoc) (same references, different UIs).


### Searching

There are a few libraries we can pick from when querying for publications. We'll use [libgen](http://gen.lib.rus.ec/) in this example with the url args <sup>*(more about the existing url args in the docs)*</sup> "dostoyevsky" as our query string and a limit of 1 publication record.

```s
curl -X GET \
  'https://freebooksapi.pyaesonemyo.me/latest/libgen/search?q=dostoyevsky&limit=1'
```

A Python equivalent example using requests:

```py
import requests

url = "https://freebooksapi.pyaesonemyo.me/latest/libgen/search?q=dostoyevsky&limit=1"

response = requests.request("GET", url)
```

Switching libraries is done through substituting the `/{library}/search` position with available librariy IDs. The exact same GET request for the above example using planetebooks would be:

```s
curl -X GET \
  'https://freebooksapi.pyaesonemyo.me/latest/planetebooks/search?q=dostoyevsky&limit=1'
```

## Contributions

For contributions: read [contributions.md](./contributions.md).
Static API Redoc at: https://pyaesonemyo.me/FreeBooksAPI/

Made with <3 by the Collaborators
