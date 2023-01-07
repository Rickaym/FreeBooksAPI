---
title: Getting Started
description: Get familiar with the API.
sidebar_position: 1
---

# Getting Started

| Type      | URL |
| ------------- |:-------------:|
| Base Url      | https://freebooksapi.pyaesonemyo.dev/api/ |
| Versioned base url      | https://freebooksapi.pyaesonemyo.dev/api/v{major} (or) https://freebooksapi.pyaesonemyo.dev/api/latest/ |
| Library selector | https://freebooksapi.pyaesonemyo.dev/api/v{major}/{library} |

To learn more about specific API endpoints, please read the [api reference](https://freebooksapi.pyaesonemyo.dev/api/latest/docs).

## Searching Example

In this example we will search for a book from [libgen](http://gen.lib.rus.ec/) library
with the query "dostoyevsky" and a limit of just 1 record for the response.

Using the versioned base url with the library selected, we get the following curl command:
```s
curl -X GET 'https://freebooksapi.pyaesonemyo.dev/api/latest/libgen/search?q=dostoyevsky&limit=1'
```

:::tip Note

You can follow along by pasting the `curl` command into the terminal.

:::

### Different Libraries

To search from different libraries, we will substituting the `{library}` url arg
from our base url with an available library ID.

The exact same GET request for the above example using planetebooks would be:

```s
curl -X GET 'https://freebooksapi.pyaesonemyo.dev/api/latest/planetebooks/search?q=dostoyevsky&limit=1'
```

A Python equivalent example using requests would simply be:

```py
import requests

url = "https://freebooksapi.pyaesonemyo.dev/api/latest/libgen/search?q=dostoyevsky&limit=1"

response = requests.request("GET", url)
```
