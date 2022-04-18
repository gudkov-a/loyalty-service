import os
import random
import string


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class CommonConfig:
    """
    Default development conf
    """
    ENV = 'development'
    MAIL_SERVER = 'test'

    DEBUG = True
    SECRET_KEY = ''.join(random.choices(string.ascii_letters, k=100))
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'migrations')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR}/app_db.sqlite')
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DO_NOT_TRUNCATE_AFTER_TEST_TABLES_LIST = ('alembic_version', )

    DEFAULT_CODE_LENGTH = 8


class TestConf(CommonConfig):
    ENV = 'testing'
    PROPAGATE_EXCEPTIONS = True
    TESTING = True


class ProdConf(CommonConfig):
    ENV = 'production'
    TESTING = False
    DEBUG = False


conf_map = {'development': CommonConfig,
            'testing': TestConf,
            'production': ProdConf}
