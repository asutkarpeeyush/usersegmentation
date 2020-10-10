import logging
import time
from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session

from db_utils.connection import Connection

Logger = logging.getLogger(__name__)


class SessionFactory:
    """
        Session manager
    """

    def __init__(self) -> None:
        """
        Gives the session factory object,This object could be created per DB

        Returns:
            None
        """
        start_time = time.time()
        self._session_factory = Connection(db_type='sqlite', db_name='db_utils.sqlite3')
        # To be used for work unit action
        self.engine = self._session_factory.engine

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
            Provide a transactional scope around a series of operations.

        Returns:
            Generator[Session, None, None]

        Raises:
            Exception
        """
        session = self._session_factory.get_session()

        try:
            yield session
            session.commit()
        except Exception:
            Logger.exception("Failed to commit")
            session.rollback()
            raise
        finally:
            session.expunge_all()
            session.close()

    def dispose_engine(self) -> None:
        """
        Disposes the session engine

        Returns:
            None
        """
        self._session_factory.dispose_engine()
