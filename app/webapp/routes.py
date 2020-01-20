def register(bp):
    @bp.route('/')
    def index():
        return "Hello, world!"
