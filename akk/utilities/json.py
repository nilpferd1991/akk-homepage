import flask

class JSONBase:
    def get_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def json_answer_with_scope(func):
    def func_wrapper(*args, **kwargs):
        from akk.db.engine import session_scope
        with session_scope() as session:
            results = func(session, *args, **kwargs)

            return flask.jsonify({"results": results})

    # Nasty stuff for app.route!
    func_wrapper.__name__ = func.__name__
    return func_wrapper