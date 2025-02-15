import os
from sqlalchemy import create_engine
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
    import dollar_data.models as models # noqa

    Base.metadata.create_all(bind=engine)
