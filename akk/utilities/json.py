import flask


class JSONBase:
    def get_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def json_answer(func):
    def func_wrapper(*args, **kwargs):
        results = func(*args, **kwargs)

        return flask.jsonify({"results": results})

    return func_wrapper