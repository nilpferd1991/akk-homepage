import json

from akk.flask_application import _app
from tests.test_db.fixtures import FullDBTestCase


class FlaskTestCase(FullDBTestCase):
    def setUp(self):
        self.app = _app.test_client()

        FullDBTestCase.setUp(self)

    def get_and_assert_result(self, get):
        result_json = self.app.get(get)
        result_dict = json.loads(result_json.data.decode())

        self.assertIn("results", result_dict)
        return_dict = result_dict["results"]

        return return_dict

    def test_list_songs(self):
        songs_dict = self.get_and_assert_result("/db/list/songs/Anoth")

        self.assertEqual(len(songs_dict), 1)
        self.assertEqual(songs_dict[0]["dance_id"], 1)
        self.assertEqual(songs_dict[0]["artist_id"], 1)
        self.assertEqual(songs_dict[0]["song_title"], "Another Test Song")
        self.assertEqual(songs_dict[0]["song_id"], 2)

        songs_dict = self.get_and_assert_result("/db/list/songs/Bla")
        self.assertEqual(len(songs_dict), 0)

    def test_list_artists(self):
        artists_dict = self.get_and_assert_result("/db/list/artists/Ar")

        self.assertEqual(len(artists_dict), 1)
        self.assertEqual(artists_dict[0]["name"], "Test Artist")
        self.assertEqual(artists_dict[0]["artist_id"], 1)

        artists_dict = self.get_and_assert_result("/db/list/artists/Bla")
        self.assertEqual(len(artists_dict), 0)

    def test_list_dances(self):
        dances_dict = self.get_and_assert_result("/db/list/dances/Ta")

        self.assertEqual(len(dances_dict), 1)
        self.assertEqual(dances_dict[0]["name"], "Tango")
        self.assertEqual(dances_dict[0]["dance_id"], 1)

        dances_dict = self.get_and_assert_result("/db/list/dances/Bla")
        self.assertEqual(len(dances_dict), 0)

    def test_list_abort(self):
        result = self.app.get("db/list/wrong")
        self.assertEqual(result.status_code, 404)

        result = self.app.get("db/list/wrong/type")
        self.assertEqual(result.status_code, 500)
