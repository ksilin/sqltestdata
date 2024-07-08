from sqlalchemy import create_engine, Column, Integer, String, Sequence, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
import os
from dotenv import load_dotenv
import uuid


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))

class Outbox(Base):
    __tablename__ = 'outbox1'
    __table_args__ = {'schema': os.getenv('DB_SCHEMA', 'public')}
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aggregatetype = Column(String, nullable=False)
    aggregateid = Column(String, nullable=False)
    type = Column(String, nullable=False)
    payload = Column(JSONB)

def get_engine():
    
    load_dotenv()
    
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', '5432')  # Default to 5432 if not set
    DB_SCHEMA = os.getenv('DB_SCHEMA', 'public')  # Default to public if not set

    if not all([DB_USER, DB_PASSWORD, DB_NAME, DB_HOST]):
        raise ValueError("Missing one or more environment variables: DB_USER, DB_PASSWORD, DB_NAME, DB_HOST")

    engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    
    # Set the schema search path
    with engine.connect() as connection:
        connection.execute(text(f'SET search_path TO {DB_SCHEMA}'))

    return engine


def create_tables(engine):
    Base.metadata.create_all(engine)
