if __name__ == "__main__":
    import json

    from main import FREEBOOKSAPI

    HTML_TEMPLATE = """<!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <title>FrebooksAPI Documentation</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
        <style>
            body {
                margin: 0;
                padding: 0;
            }
        </style>
        <style data-styled="" data-styled-version="4.4.1"></style>
    </head>
    <body>
        <div id="redoc-container"></div>
        <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"> </script>
        <script>
            var spec = %s;
            Redoc.init(spec, {}, document.getElementById("redoc-container"));
        </script>
    </body>
    </html>
    """

    with open(f"../index.html", "w") as fd:
        fd.write(HTML_TEMPLATE % json.dumps(FREEBOOKSAPI.openapi()))
