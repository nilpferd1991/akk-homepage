from tests.test_db.fixtures import DBTestCase

from akk.db.entities import *
from akk.db.engine import session_scope


class EngineTestCase(DBTestCase):
    def test_no_rollback_if_good(self):
        with session_scope() as s:
            tango = Dance(name="Tango")
            s.add(tango)

        with session_scope() as s:
            dances = s.query(Dance).all()

            self.assertEqual(len(dances), 1)
            self.assertEqual(dances[0].name, "Tango")

    def test_automatic_rollback(self):
        def will_fail_function():
            with session_scope() as s:
                tango = Dance(name="Tango")
                s.add(tango)

                bla_dance = Dance(name="Bla")
                s.add(bla_dance)

                raise AssertionError

        self.assertRaises(AssertionError, will_fail_function)

        with session_scope() as s:
            dances = s.query(Dance).all()

            self.assertEqual(len(dances), 0)
