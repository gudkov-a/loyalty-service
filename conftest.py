import pytest
from sqlalchemy import inspect
from flask.testing import Client, FlaskClient

from app import app_factory
from app import db


@pytest.fixture(scope='session', autouse=True)
def app():
    app = app_factory('testing')

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app


@pytest.fixture(autouse=True)
def clean_after_test(app):
    """
    Truncate all tables after each test module
    """
    yield
    ignored_tables = app.config['DO_NOT_TRUNCATE_AFTER_TEST_TABLES_LIST']

    for table in inspect(db.engine).get_table_names():
        if table in ignored_tables:
            continue
        db.session.execute(f'DELETE FROM {table}')
    db.session.commit()


class TestClient(Client):

    def set_auth_cookies(self):
        server_name = 'localhost'
        self.set_cookie(server_name, 'access_token', 'test')


@pytest.fixture
def client(app):
    app.test_client_class = TestClient
    return app.test_client()
