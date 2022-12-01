import re

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker

from src import config


def resolve_table_name(name: str) -> str:
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


class CustomBase:
    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__) + "s"

    def dict(self):
        """Returns a dict representation of a model."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


engine = create_engine(config.DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(cls=CustomBase)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
