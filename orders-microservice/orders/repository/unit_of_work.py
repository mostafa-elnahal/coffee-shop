from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class UnitOfWork:
    """
    Manages database sessions and transactions for the orders microservice.
    The Unit of Work pattern ensure atomicity of operations.
    """

    def __init__(self):
        """
        Initializes the UnitOfWork by creating a sessionmaker bound to the SQLite database.
        """
        self.session_maker = sessionmaker(
            bind=create_engine('sqlite:////orders.db')
        )

    def __enter__(self):
        """
        Enters the runtime context, creating a new session for the unit of work.
        This allows the UnitOfWork to be used with a 'with' statement.
        """
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        """
        Exits the runtime context, handling transaction rollback or closing the session.
        If an exception occurred, the transaction is rolled back.
        """
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()

    def commit(self):
        """
        Commits the current transaction, saving all changes made within the session to the database.
        """
        self.session.commit()

    def rollback(self):
        """
        Rolls back the current transaction, discarding all changes made within the session.
        """
        self.session.rollback()