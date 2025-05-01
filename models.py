from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.schema import ForeignKeyConstraint


class Band(Base):
    __tablename__ = "bands"

    band_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    albums = relationship("Album", back_populates="band", cascade="all, delete-orphan")


class Album(Base):
    __tablename__ = "albums"

    album_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)
    band_id = Column(Integer, ForeignKey('bands.band_id'), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['band_id'], ['bands.band_id'], ondelete='CASCADE'),
    )
    # Define relationship (optional, for easier access to band)
    band = relationship("Band", back_populates="albums")
