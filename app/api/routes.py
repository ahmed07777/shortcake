from flask import request

def register(bp):
    @bp.route('/shorten', methods=['POST'])
    def shorten_url():
        if not request.json or 'url' not in request.json:
            abort(400)
        url = request.json['url']
        # sanitize(url)
        key = core.shorten(url)
        if not key:
            abort(400)
        short_url = DOMAIN + key
        return jsonify({'short_url': short_url})


    @bp.route('/lengthen/<string:key>', methods=['GET'])
    def lengthen_url(key):
        return "Hello, world!"
