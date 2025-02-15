import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

cwd = os.getcwd()
engine = create_engine(f"sqlite:////{cwd}/database.db", echo=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():

    # even though models is not directly used, it has to imported for metadata as the Flask-SQAlchemy says so
    import dollar_data.models as models  # noqa

    # Check if tables exist before creating them
    inspector = inspect(engine)
    tables = inspector.get_table_names()  # Get a list of table names in the DB

    if "HistoricalDollar" not in tables:  # Replace with your table name
        Base.metadata.create_all(bind=engine)
        print("Tables created.")
    else:
        print("Tables already exist. Skipping creation.")
