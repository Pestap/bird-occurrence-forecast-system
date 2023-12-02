from flask import Flask
from routes.blueprint import blueprint
from flask_cors import CORS
from cache.cache_module import cache


def create_app():
    app = Flask(__name__)
    CORS(app)
    cache.init_app(app)
    return app


app = create_app()


app.register_blueprint(blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True, ssl_context= 'adhoc')
