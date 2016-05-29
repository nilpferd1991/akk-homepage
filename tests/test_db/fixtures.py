from unittest import TestCase

from akk.db.engine import session_scope
from akk.db.entities import Dance, Artist, Song, User, Playlist, Songlist


class DBTestCase(TestCase):
    def delete_all(self):
        with session_scope() as s:

            for dance in s.query(Dance).all():
                s.delete(dance)
            for artist in s.query(Artist).all():
                s.delete(artist)
            for song in s.query(Song).all():
                s.delete(song)
            for user in s.query(User).all():
                s.delete(user)
            for playlist in s.query(Playlist).all():
                s.delete(playlist)
            for songlist in s.query(Songlist).all():
                s.delete(songlist)
            s.commit()

    def tearDown(self):
        self.delete_all()