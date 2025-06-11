from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session as SQLAlchemySession
from contextlib import contextmanager
import typing

Engine = create_engine("sqlite:///data.db",echo=True)
# echo=True pra mostrar os logs de SQL gerados

Base = declarative_base()

Session = sessionmaker(bind=Engine, autoflush=False, autocommit=False)

@contextmanager
def get_session() -> typing.Generator[SQLAlchemySession, None, None]:
    db: SQLAlchemySession = Session()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    with get_session() as session:
        print("Db session iniciou com sucesso.")
print("Db session fechou com sucesso.")
