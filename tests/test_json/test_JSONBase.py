from tests.test_db.fixtures import DBTestCase

from akk.db.entities import *
from akk.db.engine import session_scope


class TestJSONBase(DBTestCase):
    def test_get_dict(self):
        with session_scope() as s:
            tango = Dance(name="Tango")
            s.add(tango)

        with session_scope() as s:
            dance = s.query(Dance).one()

            dance_dict = dance.get_dict()

            self.assertIn("dance_id", dance_dict)
            self.assertIn("name", dance_dict)
            self.assertEqual(dance_dict["name"], "Tango")


