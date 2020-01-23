Deploying Shortcake
===================

Shortcake is designed to be easily deployed to Heroku. Other cloud deployments
(including docker containers) are unsupported at this time.

To deploy to Heroku, first make sure you're logged in to your Heroku account via
the Heroku CLI. Then, run the following commands in the project root::

    $ heroku create
    $ heroku addons:create heroku-postgresql:hobby-dev
    # <domain-name> is the domain of your heroku app as output by `heroku create`
    # e.g. shrouded-ocean-06931.herokuapp.com
    $ heroku config:set DOMAIN_NAME="<domain-name>"
    # generate random data to use as a secret key
    $ heroku config:set SECRET_KEY="$(python -c 'import os; print(os.urandom(16))')"

You can then invoke the API against your Heroku instance, or browse to the root
of your Heroku app in your browser to access the web interface.

*Note:* These commands allocate resources within the limits of Heroku's free
tier. Thus an instance setup per the above will run free of charge. If you
decide to upgrade any of the Heroku components, this will no longer be the case.
