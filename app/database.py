from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Замініть user, password, host, port та db_name на ваші налаштування
DATABASE_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
