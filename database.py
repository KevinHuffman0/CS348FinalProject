from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import sqlite3


DATABASE_URL = "sqlite:///bands.db"  # SQLite Database File
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def init_db():
    connection = sqlite3.connect("bands.db")
    cursor = connection.cursor()

    # Create tables if they don’t exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bands (
            band_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS albums (
            album_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            release_year INTEGER,
            band_id INTEGER,
            FOREIGN KEY(band_id) REFERENCES bands(band_id)
        )
    ''')

    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bands_name ON bands(name);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_albums_title ON albums(title);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_albums_band_id ON albums(band_id);')

    connection.commit()
    connection.close()


def get_db_session():
    """Creates a new session for database transactions."""
    return SessionLocal()

