from dotenv import load_dotenv

load_dotenv()

from flask import Flask, Blueprint

from app.config import Config


router = Blueprint("router", __name__)


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    from app import routes

    app.register_blueprint(router)

    return app
