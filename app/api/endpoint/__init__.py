from db.engine import Session as LocalSession


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
