class Config:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///expenses.sqlite3"
    JWT_SECRET_KEY = "jwt_secret_key"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"