from sqlmodel import create_engine, Session, SQLModel
import json
# from app.config import DATABASE_URL

sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)





