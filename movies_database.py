
import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    name = Column(String(250), nullable=False)

    email = Column(String(250), nullable=False)

    picture = Column(String(250))


class Genres(Base):
    __tablename__ = 'genres'
    id = Column(
        Integer, primary_key=True)

    name = Column(
        String(250), nullable=False)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
        }


class Movies(Base):
    __tablename__ = 'movies'
    id = Column(
        Integer, primary_key=True)

    name = Column(String(250), nullable=True)

    synopsis = Column(String(250))

    release_date = Column(Integer)

    poster = Column(String(250))

    genre_id = Column(Integer, ForeignKey('genres.id'))

    genre = relationship(Genres)

    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship(User)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'release date': self.release_date,
            'synopsis': self.synopsis,
            'poster': self.poster,
            'user_id': self.user_id
        }

# insert at end of file #


engine = create_engine(
    'sqlite:///movieswithusers.db')

Base.metadata.create_all(engine)
