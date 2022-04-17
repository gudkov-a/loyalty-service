import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_marshmallow import Marshmallow

from config import conf_map

db = SQLAlchemy()
migrate = Migrate()
marshmallow = Marshmallow()
swagger = Swagger()


def add_routes(_api: Api, _app: Flask):
    import resources

    _api.add_resource(resources.CreateDiscountCode, '/api/brand/<int:brand_id>/generate_codes')
    _api.add_resource(resources.GetDiscountCode, '/api/brand/<int:brand_id>/code')
    _api.add_resource(resources.GetBrands, '/api/brands')
    _api.add_resource(resources.CustomersList, '/api/customers')

    _api.init_app(_app)


def app_factory(conf_name: str = None):
    config_name = conf_name or os.getenv('FLASK_ENV')
    if config_name is None:
        raise ValueError('Please specify FLASK_ENV variable')
    conf_obj = conf_map[config_name]

    app = Flask(__name__)
    app.config.from_object(conf_obj)

    marshmallow.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    api = Api()
    add_routes(api, app)

    return app
