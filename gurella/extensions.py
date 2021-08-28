from flask_hashing import Hashing
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
hashing = Hashing()


def init_migrate(app, database):
    return Migrate(app, database)


class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls.factory = db.create_session({})
        return cls._instance

    def get_session(self):
        return self.factory()


class Transaction:
    def __init__(self):
        self.session = SessionManager().get_session()

    def __enter__(self):
        self.session.begin()

    def execute(self, function):
        try:
            rvalue = function(db_session=self.session)
            self.session.commit()
            return rvalue
        except Exception as e:
            print(repr(e))

            self.session.rollback()
            self.session.close()

            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
