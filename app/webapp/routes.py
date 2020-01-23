from flask import request, render_template, redirect, flash, current_app
from markupsafe import Markup
from app import core


def register(bp):
    @bp.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            # the form to shorten a URL was submitted
            try:
                short_key = core.shorten_url(request.form['url'])
                short_url = 'http://{}/{}'.format(
                    current_app.config['DOMAIN_NAME'],
                    short_key)
                short_url_markup = Markup('<a href="{0}">{0}</a>'.format(short_url))
                flash(short_url_markup, 'success')
            except core.InvalidURLError:
                flash('Invalid URL. Please try again.', 'error')
            except core.OutOfShortKeysError:
                flash('Unable to shorten URL, sorry!', 'error')
        return render_template('index.html')


    @bp.route('/<string:key>', methods=['GET'])
    def short_url_redirect(key):
        try:
            expanded_url = core.lengthen_url(key)
            if not expanded_url:
                return 'not found', 404
            return redirect(expanded_url)
        except core.InvalidShortKeyError:
            # TODO
            return 'not found', 404
