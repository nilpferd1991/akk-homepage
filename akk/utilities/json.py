import flask

class JSONBase:
    def get_dict(self):
        result_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        for attr in vars(self.__class__):
            attr_value = getattr(self, attr)
            if isinstance(attr_value, JSONBase):
                result_dict.update({attr + "_" + c.name: getattr(attr_value, c.name) for c in attr_value.__table__.columns})

        return result_dict


def json_answer_with_scope(named_item):
    def decorator(func):
        def func_wrapper(*args, **kwargs):
            from akk.db.engine import session_scope
            with session_scope() as session:
                results = func(session, *args, **kwargs)

                return flask.jsonify({"results": results, "names": [song[named_item] for song in results if named_item]})

        # Nasty stuff for app.route!
        func_wrapper.__name__ = func.__name__
        return func_wrapper

    return decorator