def get_results_from_stub(s, stub, class_type, column_name=None):
    if not column_name:
        try:
            column_name = class_type.song_title
        except AttributeError:
            column_name = class_type.name

    stub_regex = "%" + stub + "%"
    results = s.query(class_type).filter(column_name.like(stub_regex)).all()

    return [r.get_dict() for r in results]