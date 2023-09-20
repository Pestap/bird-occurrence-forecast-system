from flask import Flask
from routes.blueprint import blueprint


def create_app():
    app = Flask(__name__)
    return app


app = create_app()
app.register_blueprint(blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)
