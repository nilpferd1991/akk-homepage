from unittest import TestCase

from akk.db.entities import *
from akk.db.engine import get_session


class TestDance(TestCase):

    def setUp(self):
        self.delete_all()

        s = get_session()
        tango = Dance(name="Tango")
        s.add(tango)

        artist = Artist(name="Test Artist")
        s.add(artist)

        song = Song(song_title="Test Song", artist=artist, dance=tango)
        s.add(song)

        another_song = Song(song_title="Another Test Song", artist=artist, dance=tango)
        s.add(song)

        user = User(name="Herbert", password_hash="1", password_salt="2")
        s.add(user)

        playlist = Playlist(user=user, songs=[song, another_song])
        s.add(playlist)

        s.commit()

    def delete_all(self):
        s = get_session()

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

    def test_dance(self):
        s = get_session()

        dances = s.query(Dance).all()

        self.assertEqual(len(dances), 1)
        self.assertEqual(dances[0].name, "Tango")

    def test_artist(self):
        s = get_session()

        artists = s.query(Artist).all()

        self.assertEqual(len(artists), 1)
        self.assertEqual(artists[0].name, "Test Artist")

    def test_song(self):
        s = get_session()

        songs = s.query(Song).all()

        self.assertEqual(len(songs), 2)
        self.assertEqual(songs[0].song_title, "Test Song")
        self.assertEqual(songs[0].artist.name, "Test Artist")
        self.assertEqual(songs[0].dance.name, "Tango")

    def test_users(self):
        s = get_session()

        users = s.query(User).all()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, "Herbert")

    def test_playlists(self):
        s = get_session()

        playlists = s.query(Playlist).all()

        self.assertEqual(len(playlists), 1)
        self.assertEqual(playlists[0].user.name, "Herbert")
        self.assertEqual(len(playlists[0].songs), 2)
        self.assertEqual(playlists[0].songs[0].song_title, "Test Song")
        self.assertEqual(playlists[0].songs[1].song_title, "Another Test Song")

    def test_delete_artist(self):
        s = get_session()

        artist = s.query(Artist).one()
        s.delete(artist)
        s.commit()

        self.assertEqual(len(s.query(Artist).all()), 0)
        self.assertEqual(len(s.query(Dance).all()), 1)
        self.assertEqual(len(s.query(Song).all()), 0)
        self.assertEqual(len(s.query(Songlist).all()), 0)
        self.assertEqual(len(s.query(Playlist).all()), 1)
        self.assertEqual(len(s.query(User).all()), 1)

    def test_delete_song(self):
        s = get_session()

        song = s.query(Song).first()
        s.delete(song)
        s.commit()

        self.assertEqual(len(s.query(Artist).all()), 1)
        self.assertEqual(len(s.query(Dance).all()), 1)
        self.assertEqual(len(s.query(Song).all()), 1)
        self.assertEqual(len(s.query(Songlist).all()), 1)
        self.assertEqual(len(s.query(Playlist).all()), 1)
        self.assertEqual(len(s.query(User).all()), 1)

    def test_delete_dance(self):
        s = get_session()

        dance = s.query(Dance).one()
        s.delete(dance)
        s.commit()

        self.assertEqual(len(s.query(Artist).all()), 1)
        self.assertEqual(len(s.query(Dance).all()), 0)
        self.assertEqual(len(s.query(Song).all()), 0)
        self.assertEqual(len(s.query(Songlist).all()), 0)
        self.assertEqual(len(s.query(Playlist).all()), 1)
        self.assertEqual(len(s.query(User).all()), 1)

    def test_delete_user(self):
        s = get_session()

        user = s.query(User).one()
        s.delete(user)
        s.commit()

        self.assertEqual(len(s.query(Artist).all()), 1)
        self.assertEqual(len(s.query(Dance).all()), 1)
        self.assertEqual(len(s.query(Song).all()), 2)
        self.assertEqual(len(s.query(Songlist).all()), 0)
        self.assertEqual(len(s.query(Playlist).all()), 0)
        self.assertEqual(len(s.query(User).all()), 0)

    def test_delete_playlist(self):
        s = get_session()

        playlist = s.query(Playlist).one()
        s.delete(playlist)
        s.commit()

        self.assertEqual(len(s.query(Artist).all()), 1)
        self.assertEqual(len(s.query(Dance).all()), 1)
        self.assertEqual(len(s.query(Song).all()), 2)
        self.assertEqual(len(s.query(Songlist).all()), 0)
        self.assertEqual(len(s.query(Playlist).all()), 0)
        self.assertEqual(len(s.query(User).all()), 1)
