import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

IS_VERCEL = os.environ.get("VERCEL") == "1"
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    if IS_VERCEL:
        DATABASE_URL = "sqlite://"
    else:
        db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        os.makedirs(db_dir, exist_ok=True)
        DATABASE_URL = f"sqlite:///{os.path.join(db_dir, 'bharatproblembase.db')}"

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

_is_sqlite = DATABASE_URL.startswith("sqlite")

_engine_kwargs = {
    "pool_pre_ping": True,
    "connect_args": connect_args,
}

if not _is_sqlite:
    _engine_kwargs["pool_size"] = 5
    _engine_kwargs["max_overflow"] = 10

engine = create_engine(DATABASE_URL, **_engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models.problem_statement import ProblemStatement
    from app.models.user import User
    Base.metadata.create_all(bind=engine)
