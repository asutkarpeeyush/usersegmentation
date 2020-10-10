from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_utils.models import Base


class Connection:
    DB_ENGINE = {
        "sqlite": 'sqlite:///{DB}'
    }

    def __init__(self, db_type, db_name, username="", password=""):
        db_type = db_type.lower()
        if db_type in self.DB_ENGINE:
            engine_url = self.DB_ENGINE[db_type].format(DB=db_name)
            self.engine = create_engine(engine_url)
        else:
            raise Exception(f"DB type {db_type} is not supported.")

        # create DB tables
        self.__create_db_tables()

        # Init Session
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def __create_db_tables(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    def dispose_engine(self) -> None:
        self.engine.dispose()




