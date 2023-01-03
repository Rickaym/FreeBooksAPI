---
sidebar_position: 1
---

# Getting Started

We'll need to keep in mind the following base URLs to understand the whole API.

| Type      | Url |
| ------------- |:-------------:|
| Base Url      | https://freebooksapi.pyaesonemyo.me/ |
| Versioned base url      | https://freebooksapi.pyaesonemyo.me/v{major} (or) /latest/ |
| Library selector | https://freebooksapi.pyaesonemyo.me/v{major}/{library} |

For specific API Reference, look at [redoc](https://freebooksapi.pyaesonemyo.me/latest/api-reference).

### Searching Example

There are a few libraries we can pick from when querying for publications. We'll use [libgen](http://gen.lib.rus.ec/) in this example with the url args <sup>*(more about the existing url args in the docs)*</sup> "dostoyevsky" as our query string and a limit of 1 publication record.

Using the versioned base url with the library selected, we get the following curl command:
```s
curl -X GET \
  'https://freebooksapi.pyaesonemyo.me/latest/libgen/search?q=dostoyevsky&limit=1'
```

:::tip Note

You don't need any authorization to use this API. Please use judiciously lol.

:::

#### Different Libraries

Switching libraries is simply done through substituting the `{library}` url arg from our base url with an available library ID.

The exact same GET request for the above example using planetebooks would be:

```s
curl -X GET \
  'https://freebooksapi.pyaesonemyo.me/latest/planetebooks/search?q=dostoyevsky&limit=1'
```

A Python equivalent example using requests would simply be:

```py
import requests

url = "https://freebooksapi.pyaesonemyo.me/latest/libgen/search?q=dostoyevsky&limit=1"

response = requests.request("GET", url)
```

