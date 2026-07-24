from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.types import TypeDecorator, String
import uuid
from app.core.config import settings


class UUID_TYPE(TypeDecorator):
    impl = String(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(value)


engine = None
SessionLocal = None


class Base(DeclarativeBase):
    pass


def get_db_url():
    url = settings.database_url
    if "postgresql" not in url:
        return url
    try:
        import psycopg2
        return url
    except ImportError:
        return "sqlite:///./interservim_ai.db"


def init_db():
    global engine, SessionLocal
    if engine is None:
        db_url = get_db_url()
        connect_args = {}
        if db_url.startswith("sqlite"):
            connect_args["check_same_thread"] = False
        engine = create_engine(db_url, pool_pre_ping=True, connect_args=connect_args if connect_args else {})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


def get_db():
    _, session = init_db()
    db = session()
    try:
        yield db
    finally:
        db.close()
