# FreeBooksAPI 🏛️

<a href="https://freebooksapi.pyaesonemyo.me/latest/docs"><img alt="swagger-ui-docs" src="https://img.shields.io/badge/swagger-docs-brightgreen?style=for-the-badge&logo=swagger"></a>
<a href="https://freebooksapi.pyaesonemyo.me/latest/redoc"><img alt="redoc-docs" src="https://img.shields.io/badge/Redoc-docs-purple?style=for-the-badge&logo=Read the Docs&logoColor=violet"></a>

A comprehensive (unofficial) API service for [planet-ebooks](https://www.planetebook.com/), [gen.lib.rus.ec/libgen.rs](http://gen.lib.rus.ec/), [libgen.lc/libgen.li](http://libgen.lc/), providing API endpoints to retrieve download URLs, mirrors, publication metadata, and the likes.


## Tech Stack

<img alt="hosted-on-vultr" src="https://img.shields.io/badge/server-vultr-blue?style=for-the-badge&logo=vultr&logoColor=51B9FF">
<img alt="load-balanced-with-nginx" src="https://img.shields.io/badge/scale-nginx-009137?style=for-the-badge&logo=nginx&logoColor=green">
<img alt="built-with-docker" src="https://img.shields.io/badge/build-docker-0F6AAA?style=for-the-badge&logo=docker">
<img alt="based-on-fastapi" src="https://img.shields.io/badge/ASGI-fastapi-F7CA3E?style=for-the-badge&logo=fastapi&logoColor=F7CA3E">

## Features

- Searching books by name, author name, topic and etc...
- Retrieve free download URLs for books and publications
- Retrieve torrent datadumps for free books

## Getting Started

We'll need to keep in mind the following base URLs to understand the whole API.

| Base Url      | https://freebooksapi.pyaesonemyo.me/ |
| ------------- |:-------------:|
| Versioned base url      | https://freebooksapi.pyaesonemyo.me/v{major} (or) /latest/ |
| Library selector | https://freebooksapi.pyaesonemyo.me/v{major}/{library} |

For specific API Reference, look at [Swagger Docs](https://freebooksapi.pyaesonemyo.me/latest/docs) or [ReDoc](https://freebooksapi.pyaesonemyo.me/latest/redoc) (same documentation, different UIs).


### Searching Example

There are a few libraries we can pick from when querying for publications. We'll use [libgen](http://gen.lib.rus.ec/) in this example with the url args <sup>*(more about the existing url args in the docs)*</sup> "dostoyevsky" as our query string and a limit of 1 publication record.

Using the versioned base url with the library selected, we get the following curl command:
```s
curl -X GET \
  'https://freebooksapi.pyaesonemyo.me/latest/libgen/search?q=dostoyevsky&limit=1'
```

a Python equivalent example using requests would simply be:

```py
import requests

url = "https://freebooksapi.pyaesonemyo.me/latest/libgen/search?q=dostoyevsky&limit=1"

response = requests.request("GET", url)
```

#### Different Libraries

Switching libraries is simply done through substituting the `{library}` url arg from our base url with an available library ID.

The exact same GET request for the above example using planetebooks would be:

```s
curl -X GET \
  'https://freebooksapi.pyaesonemyo.me/latest/planetebooks/search?q=dostoyevsky&limit=1'
```

```diff
+ Note: You don't need any authorization to use this API.
```
 Happy Coding!

## Support the Project

Kindly consider supporting this project through starring the repository or buying me a coffee to cover the server costs! :D And thanks a lot for using our API, it's always extremely gratifying seeing your work help other people.

<a href="https://www.buymeacoffee.com/rickaym" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

## Contributions

For contributions: read [contributions.md](./contributions.md).

Made with <3 by the Collaborators
