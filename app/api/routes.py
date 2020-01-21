from flask import current_app, request, abort, jsonify
from app import core


def register(bp):
    @bp.route('/shorten', methods=['POST'])
    def shorten():
        if not request.json or 'url' not in request.json:
            abort(400)
        try:
            url = request.json['url']
            key = core.shorten_url(url)
            short_url = 'http://{}/{}'.format(
                current_app.config['DOMAIN_NAME'],
                key)
            return jsonify({'short_url': short_url})
        except core.InvalidURLError as e:
            # TODO more descriptive and individualized error messages
            abort(400)
        except core.OutOfShortKeysError as e:
            abort(400)


    @bp.route('/lengthen/<string:key>', methods=['GET'])
    def lengthen(key):
        try:
            url = core.lengthen_url(key)
            return jsonify({'url': url})
        except core.InvalidShortKeyError as e:
            abort(400)
