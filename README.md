# :cake: Shortcake :cake:

**Shortcake** is a URL shortening service. It provides a RESTful API that allows
URLs to be both shortened and lengthened, as well as a simple web interface to
the same functionality. Shortcake can easily be deployed to the cloud, allowing
anyone to host their own URL shortener.

## Shortcake in action

Assuming you're running the development server locally, the API works like this:
``` bash
$ curl -i -H "Content-Type: application/json" -X POST -d '{"url": "http://www.google.com/"}' http://localhost:5000/api/v1/shorten
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 51
Server: Werkzeug/0.16.0 Python/3.8.1
Date: Wed, 22 Jan 2020 19:41:33 GMT

{"short_url": "http://localhost:5000/qOtlLcV"}

$ curl -i http://localhost:5000/api/v1/lengthen/qOtlLcV
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 38
Server: Werkzeug/0.16.0 Python/3.8.1
Date: Wed, 22 Jan 2020 19:42:23 GMT

{"url": "http://www.google.com/"}
```

It's that simple!

## Deployment

Shortcake is designed to be easily deployed to Heroku. Other cloud deployments
(including docker containers) are unsupported at this time.

To deploy to Heroku, first make sure you're logged in to your Heroku account via
the Heroku CLI. Then, run the following commands in the project root:
``` bash
$ heroku create
$ heroku addons:create heroku-postgresql:hobby-dev
# <domain-name> is the domain of your heroku app as output by `heroku create`
# e.g. shrouded-ocean-06931.herokuapp.com
$ heroku config:set DOMAIN_NAME="<domain-name>"
# generate random data to use as a secret key
$ heroku config:set SECRET_KEY="$(python -c 'import os; print(os.urandom(16))')"
$ git push heroku master
$ heroku open
```

You can then invoke the API against your Heroku instance, or browse to the root
of your Heroku app in your browser to access the web interface.

*Note:* These commands allocate resources within the limits of Heroku's free
tier. Thus an instance setup per the above will run free of charge. If you
decide to upgrade any of the Heroku components, this will no longer be the case.

## Development

If you wish to hack on shortcake yourself, you will find the contents of the
`scripts/` directory useful. In particular, the developer documentation can be
built locally using `scripts/build-docs`, the development server can be run
using `scripts/run-dev`, and the interactive shell instance of the application
can be invoked using `scripts/run-shell`.

Note that both building the docs and running the tests require you to install
the development dependencies via `pipenv install -d`.
