<img width="400px" src="https://raw.githubusercontent.com/Rickaym/FreeBooksAPI/bd035158db4bc9363e1b00d0bd3221183cc94ad7/assets/logo.png">

<!-- header -->

<a href="https://freebooksapi.pyaesonemyo.dev/latest/docs"><img alt="redoc-docs" src="https://img.shields.io/badge/Redoc-docs-purple?style=for-the-badge&logo=Read the Docs&logoColor=violet"></a>
<a href="https://discord.gg/UmnzdPgn6g/"><img src="https://img.shields.io/discord/793047973751554088.svg?label=API Support&color=blue&style=for-the-badge&logo=discord" alt="Discord"></a>

A comprehensive (unofficial) API service for [planet-ebooks](https://www.planetebook.com/), [gen.lib.rus.ec/libgen.rs](http://gen.lib.rus.ec/), [libgen.lc/libgen.li](http://libgen.lc/), providing API endpoints to retrieve download URLs, mirrors, publication metadata, and the likes.

The API implements the following features:

- Searching for publications and books by name, author name, topic, and so on.
- Retrieve download URLs for books and publications
- Retrieve datadumps sites for libraries
- Retrieve library aliases list


## Tech Stack

<img alt="hosted-on-vultr" src="https://img.shields.io/badge/server-vultr-blue?style=for-the-badge&logo=vultr&logoColor=51B9FF">
<img alt="load-balanced-with-nginx" src="https://img.shields.io/badge/scale-nginx-009137?style=for-the-badge&logo=nginx&logoColor=green">
<img alt="built-with-docker" src="https://img.shields.io/badge/build-docker-0F6AAA?style=for-the-badge&logo=docker">
<img alt="based-on-fastapi" src="https://img.shields.io/badge/ASGI-fastapi-F7CA3E?style=for-the-badge&logo=fastapi&logoColor=F7CA3E">

## Getting Started

We'll need to keep in mind the following base URLs to understand the whole API.

| Base Url      | https://freebooksapi.pyaesonemyo.dev/ |
| ------------- |:-------------:|
| Versioned base url      | https://freebooksapi.pyaesonemyo.dev/v{major} (or) /latest/ |
| Library selector | https://freebooksapi.pyaesonemyo.dev/v{major}/{library} |

For specific API Reference, look at [ReDoc](https://freebooksapi.pyaesonemyo.dev/latest/docs).

### Searching Example

There are a few libraries we can pick from when querying for publications. We'll use [libgen](http://gen.lib.rus.ec/) in this example with the url args <sup>*(more about the existing url args in the docs)*</sup> "dostoyevsky" as our query string and a limit of 1 publication record.

Using the versioned base url with the library selected, we get the following curl command:
```s
curl -X GET \
  'https://freebooksapi.pyaesonemyo.dev/latest/libgen/search?q=dostoyevsky&limit=1'
```

#### Different Libraries

Switching libraries is simply done through substituting the `{library}` url arg from our base url with an available library ID.

The exact same GET request for the above example using planetebooks would be:

```s
curl -X GET \
  'https://freebooksapi.pyaesonemyo.dev/latest/planetebooks/search?q=dostoyevsky&limit=1'
```

A Python equivalent example using requests would simply be:

```py
import requests

url = "https://freebooksapi.pyaesonemyo.dev/latest/libgen/search?q=dostoyevsky&limit=1"

response = requests.request("GET", url)
```

```diff
+ Note: You don't need any authorization to use this API.
```

## Support the Project

Kindly consider supporting this project through starring the repository or buying me a coffee to cover the server costs! Thanks a lot for using our API, it's always extremely gratifying seeing your work help other people.

<a href="https://www.buymeacoffee.com/rickaym" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 45px" ></a>

### Contributions

For contributions: read [contributions](./contributions.md).

Made with <3 by the Collaborators
