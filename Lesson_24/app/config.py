import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_NAME = os.getenv('DATABASE')
    DB_CITY = os.getenv('DATABASE_CITY')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
