from database.connection import Session

def db_session():
    try:
        session = Session()
        yield session

    finally:
        session.close()