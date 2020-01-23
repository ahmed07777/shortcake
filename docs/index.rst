.. Shortcake documentation master file, created by
   sphinx-quickstart on Sun Jan 19 14:49:24 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Shortcake -- Deliciously short URLs
=====================================

**Shortcake** is a URL shortening service. It provides a RESTful API that allows
URLS to be both shortened and lengthened, as well as a simple web interface to
the same functionality. Shortcake can easily be deployed to the cloud, allowing
anyone to host their own URL shortener.

Shortcake in action
-------------------

Assuming you're running the development server locally, the API works like this::

    $ curl -i -H "Content-Type: application/json" -X POST -d '{"url": "http://www.google.com/"}' http://localhost:5000/api/v1/shorten
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 51
    Server: Werkzeug/0.16.0 Python/3.8.1
    Date: Wed, 22 Jan 2020 19:41:33 GMT

    {
      "short_url": "http://localhost:5000/qOtlLcV"
    }

    $ curl -i http://localhost:5000/api/v1/lengthen/qOtlLcV
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 38
    Server: Werkzeug/0.16.0 Python/3.8.1
    Date: Wed, 22 Jan 2020 19:42:23 GMT

    {
      "url": "http://www.google.com/"
    }

It's that simple!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   deployment
   rest_api
   modules
