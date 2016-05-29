import flask
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

class JSONBase:
    def get_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def get_json(self):
        flask.jsonify(self.get_dict())


Base = declarative_base(cls=JSONBase)

class Dance(Base):
    __tablename__ = 'dances'
    dance_id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)

    def __repr__(self):
        return "Dance: {self.name} ({self.dance_id})".format(self=self)


class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)

    def __repr__(self):
        return "Artist: {self.name} ({self.artist_id})".format(self=self)


class Song(Base):
    __tablename__ = "songs"
    song_id = Column(Integer, primary_key=True)
    song_title = Column(String(350), nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    # Delete when artists is deleted
    artist = relationship(Artist, backref=backref("songs", uselist=True, cascade='delete,all'))
    dance_id = Column(Integer, ForeignKey('dances.dance_id'))
    # Delete when dance is deleted
    dance = relationship(Dance, backref=backref("songs", uselist=True, cascade='delete,all'))

    def __repr__(self):
        return "Song: {self.song_title} ({self.song_id}) - {self.artist} - {self.dance}".format(self=self)


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)
    password_salt = Column(String(100), nullable=False)

    def __repr__(self):
        return "User: {self.name} ({self.user_id})".format(self=self)


class Playlist(Base):
    __tablename__ = 'playlists'
    playlist_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    # Delete when user is deleted
    user = relationship(User, backref=backref("playlists", uselist=True, cascade="delete,all"))
    songs = relationship(Song, secondary="songlists")

    def __repr__(self):
        return "Playlist: {self.user} - {self.songs}".format(self=self)


class Songlist(Base):
    __tablename__ = "songlists"
    song_id = Column(Integer, ForeignKey("songs.song_id"), primary_key=True)
    # Delete empty songlists
    song = relationship(Song, backref=backref("songlists", uselist=True, cascade="delete,all"))
    playlist_id = Column(Integer, ForeignKey("playlists.playlist_id"), primary_key=True)

    def __repr__(self):
        return "Songlist: {self.song_id} - {self.playlist_id}".format(self=self)